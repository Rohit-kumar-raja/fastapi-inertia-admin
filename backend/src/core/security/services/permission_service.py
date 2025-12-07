from typing import List, Optional
from sqlalchemy.orm import selectinload, with_loader_criteria
from uuid import UUID
from datetime import datetime
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.privilege_model import PrivilegeModel

from ..models.privilege_permission_link_model import PrivilegeRouteLinkModel
from ..models.route_model import RouteModel


class PermissionService:
    """
    PermissionService handles the business logic and database operations for Permission.
    """

    @staticmethod
    async def create(data: dict, session: AsyncSession) -> RouteModel:
        """Create a new Route."""
        try:
            privilege_ids = data.pop("privilege_ids", [])
            privileges = await session.execute(select(PrivilegeModel).where(PrivilegeModel.id.in_(privilege_ids)))
            privileges = privileges.scalars().all()
            instance = RouteModel(**data)
            instance.privileges = privileges

            session.add(instance)
            await session.commit()  # Ensure instance.id is available
            await session.refresh(instance)
            return instance
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_all(session: AsyncSession) -> List[RouteModel]:
        """Fetch all active and non-deleted Route."""
        statement = (
            select(RouteModel, RouteModel)
            .where(RouteModel.deleted_at.is_(None))
            .options(
                # selectinload(RouteModel.children),
                selectinload(RouteModel.privileges)
                # with_loader_criteria(
                #     RouteModel,  # Applies to RouteModel's children
                #     RouteModel.deleted_at.is_(None) & RouteModel.is_active.is_(True),
                #     include_aliases=True,  # Necessary when dealing with relationships
                # ),
            )
        )
        result = await session.execute(statement)
        routes = result.scalars().unique().all()
        return routes

    @staticmethod
    async def get_by_id(uuid: UUID, session: AsyncSession) -> Optional[RouteModel]:
        """Fetch a Route by its UUID."""
        statement = (
            select(RouteModel)
            .where(
                RouteModel.id == uuid,
                RouteModel.deleted_at.is_(None),
            )
            .options(
                selectinload(RouteModel.privileges),
                selectinload(RouteModel.children).options(
                    selectinload(RouteModel.children)  # This enables n-level deep loading
                ),
                with_loader_criteria(
                    RouteModel,  # Applies to RouteModel's children
                    RouteModel.deleted_at.is_(None),
                    include_aliases=True,  # Necessary when dealing with relationships
                ),
            )
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def update(uuid: UUID, data: dict, session: AsyncSession) -> Optional[RouteModel]:
        """Update an existing Permission."""
        async with session.begin():
            data.pop("id", None)
            if "privilege_ids" in data:
                privilege_ids = data.pop("privilege_ids")
                await session.execute(
                    delete(PrivilegeRouteLinkModel).where(PrivilegeRouteLinkModel.auth_route_id == uuid)
                )

                for privilege_id in privilege_ids:
                    privilege_permission_link = PrivilegeRouteLinkModel(
                        auth_privilege_id=privilege_id, auth_route_id=uuid
                    )
                    session.add(privilege_permission_link)

            await session.execute(
                update(RouteModel)
                .where(
                    RouteModel.id == uuid,
                    RouteModel.deleted_at.is_(None),
                )
                .values(**data)
            )
        return await PermissionService.get_by_id(uuid, session)

    @staticmethod
    async def delete(uuid: UUID, session: AsyncSession) -> bool:
        """Soft delete a Permission by its UUID."""
        instance = await session.get(RouteModel, uuid)
        if instance and instance.deleted_at is None:
            instance.deleted_at = datetime.utcnow()
            await session.commit()
            return True
        return False

    @staticmethod
    async def is_unique(name: str, parent_id: UUID, session: AsyncSession) -> bool:
        """Check if a permission with the same name and parent_id exists."""
        statement = select(RouteModel).where(
            RouteModel.name == name,
            RouteModel.parent_id == parent_id,
            RouteModel.deleted_at.is_(None),
        )
        result = await session.execute(statement)
        return result.scalars().first() is not None

    @staticmethod
    async def get_permission_tree(session: AsyncSession):
        """Fetch all routes and structure them as a hierarchy."""
        statement = (
            select(RouteModel)
            .where(RouteModel.deleted_at.is_(None))
            .options(
                selectinload(RouteModel.children),
                with_loader_criteria(RouteModel, RouteModel.deleted_at.is_(None)),
                selectinload(RouteModel.privileges),
            )
        )

        result = await session.execute(statement)
        routes = result.scalars().all()
        # Filter the root-level permissions (those without a parent)
        tree = [perm for perm in routes if perm.parent_id is None]

        def serialize(perm):
            return {
                "id": str(perm.id),
                "name": perm.name,
                "parent_id": str(perm.parent_id) if perm.parent_id else None,
                "is_active": perm.is_active,
                "created_at": perm.created_at.isoformat(),
                "children": [serialize(child) for child in perm.children],  # Ensure correct child hierarchy
            }

        return list(map(serialize, tree))
