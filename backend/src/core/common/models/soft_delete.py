from datetime import datetime
from sqlalchemy import DateTime, event, inspect, Index, UniqueConstraint, Table, select, func
from sqlalchemy.orm import with_loader_criteria, Session, Mapper, Mapped, mapped_column, with_parent
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs


class AsyncSoftDelete(AsyncAttrs):
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    @classmethod
    def __declare_last__(cls):
        """
        Runs after model mapping. Converts 'unique=True' constraints
        to Partial Indexes (WHERE deleted_at IS NULL).
        """
        table: Table = cls.__table__

        constraints_to_remove = []
        indexes_to_add = []

        # Iterate over constraints
        for constraint in list(table.constraints):
            if isinstance(constraint, UniqueConstraint):
                # FIX: Removed "if constraint in table.primary_key:"
                # PrimaryKeyConstraint is NOT a UniqueConstraint subclass,
                # so the isinstance check above already filters out PKs.

                # Generate Index Name if missing
                index_name = constraint.name
                if not index_name:
                    col_names = "_".join([c.name for c in constraint.columns])
                    index_name = f"uq_{table.name}_{col_names}"

                # Create the Partial Index
                new_index = Index(
                    index_name,
                    *constraint.columns,
                    unique=True,
                    postgresql_where=cls.deleted_at.is_(None),
                    sqlite_where=cls.deleted_at.is_(None),
                )

                constraints_to_remove.append(constraint)
                indexes_to_add.append(new_index)

        # Apply changes to the Table
        for const in constraints_to_remove:
            table.constraints.discard(const)

            # IMPORTANT: Explicitly disable unique=True on the columns
            # so Alembic doesn't try to recreate the standard constraint.
            for col in const.columns:
                col.unique = False

        for idx in indexes_to_add:
            table.indexes.add(idx)

    async def delete(self, session: AsyncSession):
        if self.deleted_at is not None:
            return
        self.deleted_at = datetime.now()

        mapper: Mapper = inspect(self.__class__)
        for relationship in mapper.relationships:
            if relationship.cascade.delete:
                related_objects = await getattr(self.awaitable_attrs, relationship.key)
                if related_objects:
                    if isinstance(related_objects, list):
                        for child in related_objects:
                            if isinstance(child, AsyncSoftDelete):
                                await child.delete(session)
                    elif isinstance(related_objects, AsyncSoftDelete):
                        await related_objects.delete(session)

    def restore(self):
        self.deleted_at = None

    @classmethod
    async def get_child_counts_by_id(cls, session: AsyncSession, record_id):
        """
        Returns a dictionary of {relationship_name: count} for all children.
        """
        mapper: Mapper = inspect(cls)
        summary = {}

        # Create a dummy instance with just the PK so with_parent can generate the SQL
        # This avoids fetching the parent object from DB first
        pk_name = mapper.primary_key[0].name
        dummy_instance = cls(**{pk_name: record_id})

        for rel in mapper.relationships:
            # We only want to count children (One-to-Many), not parents (Many-to-One)
            if rel.direction.name == "MANYTOONE":
                continue

            label = rel.key
            child_class = rel.mapper.class_

            # FIX: Use getattr(cls, rel.key) to get the actual relationship attribute
            # 'rel.key' is just a string (e.g. "items"), but with_parent needs Model.items
            relationship_attr = getattr(cls, rel.key)

            stmt = select(func.count()).select_from(child_class).where(with_parent(dummy_instance, relationship_attr))

            # Execute sequentially to avoid AsyncSession concurrency errors
            result = await session.execute(stmt)
            summary[label] = result.scalar()

        return summary


def register_async_soft_delete_listener(ignored_session_cls=None):
    @event.listens_for(Session, "do_orm_execute")
    def _add_filtering_criteria(execute_state):
        if execute_state.is_select:
            execute_state.statement = execute_state.statement.options(
                with_loader_criteria(
                    AsyncSoftDelete,
                    lambda cls: cls.deleted_at.is_(None),
                    include_aliases=True,
                )
            )


register_async_soft_delete_listener()
