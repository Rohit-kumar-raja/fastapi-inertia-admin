from typing import List, Optional
from uuid import UUID

from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.permission_model import PermissionModel
from ..models.role_model import RoleModel, RolePermissionLinkModel
from datatables import DataTables, DataTablesRequest, DataTablesResponse


class RoleService:
    """
    RoleService handles the business logic and database operations for Role.
    """

    @staticmethod
    async def create(data: dict, session: AsyncSession) -> Optional[RoleModel]:
        """Create a new Role."""
        try:
            permission_ids = data.pop("permission_ids", [])
            permissions = await session.execute(select(PermissionModel).where(PermissionModel.id.in_(permission_ids)))
            permissions = permissions.unique().scalars().all()
            instance = RoleModel(**data)

            instance.permissions = permissions
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_all(session: AsyncSession) -> List[dict]:
        """Fetch all Roles."""
        statement = (
            select(RoleModel)
            .where(RoleModel.deleted_at.is_(None))
            .options(selectinload(RoleModel.permissions))
        )
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(uuid: UUID, session: AsyncSession) -> Optional[dict]:
        """Fetch a Role by its UUID."""
        statement = (
            select(RoleModel)
            .where(
                RoleModel.id == uuid,
                RoleModel.deleted_at.is_(None),
            )
            .options(selectinload(RoleModel.permissions))
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def update(uuid: UUID, data: dict, session: AsyncSession) -> Optional[dict]:
        """Update an existing Role."""
        try:
            async with session.begin():
                data.pop("id", None)
                if "permission_ids" in data:
                    permission_ids = data.pop("permission_ids")
                    await session.execute(
                        delete(RolePermissionLinkModel).where(RolePermissionLinkModel.auth_role_id == uuid)
                    )
                    for permission_id in permission_ids:
                        session.add(RolePermissionLinkModel(auth_permission_id=permission_id, auth_role_id=uuid))
                await session.execute(
                    update(RoleModel).where(RoleModel.id == uuid, RoleModel.deleted_at.is_(None)).values(**data)
                )
            await session.commit()
            return await RoleService.get_by_id(uuid, session)
        except SQLAlchemyError:
            await session.rollback()
            return None

    @staticmethod
    async def delete(uuid: UUID, session: AsyncSession) -> bool:
        """Soft delete a Role if it is active and not already deleted."""
        instance = await session.get(RoleModel, uuid)
        if instance and instance.deleted_at is None:
            instance.deleted_at = datetime.utcnow()
            await session.commit()
            await session.refresh(instance)
            return True
        return False

    @staticmethod
    async def is_unique(name: str, session: AsyncSession) -> bool:
        statement = select(RoleModel).where(
            RoleModel.name == name,
            RoleModel.deleted_at.is_(None),
        )
        result = await session.execute(statement)
        return result.scalars().first() is not None

    @staticmethod
    async def datatables(session: AsyncSession, request_data: DataTablesRequest) -> List[RoleModel]:
        """Fetch all active and non-deleted Roles."""
        statement = (
            select(RoleModel)
            .filter_by(deleted_at=None, is_active=True)
            .options(selectinload(RoleModel.permissions))
        )
        datatables = DataTables(session, RoleModel, statement)
        return await datatables.process(request_data=request_data)
