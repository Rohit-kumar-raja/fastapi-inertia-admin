from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import selectinload
from ..models.privilege_model import PrivilegeModel
from datatables import DataTables, DataTablesRequest


class PrivilegeService:
    """
    PrivilegeService handles the business logic and database operations for Privilege.
    """

    @staticmethod
    async def create(data: dict, session: AsyncSession) -> PrivilegeModel:
        """Create a new Privilege."""
        instance = PrivilegeModel(**data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @staticmethod
    async def get_all(session: AsyncSession) -> List[PrivilegeModel]:
        """Fetch all active and non-deleted Privileges."""
        statement = select(PrivilegeModel).where(PrivilegeModel.deleted_at.is_(None))
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(uuid: UUID, session: AsyncSession) -> Optional[PrivilegeModel]:
        """Fetch an active and non-deleted Privilege by its UUID."""
        statement = select(PrivilegeModel).where(PrivilegeModel.id == uuid, PrivilegeModel.deleted_at.is_(None))
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def update(uuid: UUID, data: dict, session: AsyncSession) -> Optional[PrivilegeModel]:
        """Update an existing Privilege if it is active and not deleted."""
        async with session.begin():
            data.pop("id", None)
            statement = (
                update(PrivilegeModel)
                .where(PrivilegeModel.id == uuid, PrivilegeModel.deleted_at.is_(None))
                .values(**data)
            )
            await session.execute(statement)
        return await PrivilegeService.get_by_id(uuid, session)

    @staticmethod
    async def delete(uuid: UUID, session: AsyncSession) -> bool:
        """Soft delete a Privilege if it is active and not already deleted."""
        instance = await session.get(PrivilegeModel, uuid)
        if instance and instance.deleted_at is None:
            instance.deleted_at = datetime.now()
            await session.commit()
            return True
        return False

    @staticmethod
    async def is_unique(access: str, session: AsyncSession) -> bool:
        """Check if a privilege with the same access already exists."""
        statement = select(PrivilegeModel).where(PrivilegeModel.access == access, PrivilegeModel.deleted_at.is_(None))
        result = await session.execute(statement)
        return result.scalars().first() is not None

    @staticmethod
    async def datatables(session: AsyncSession, request_data: DataTablesRequest) -> List[PrivilegeModel]:
        """Fetch all active and non-deleted Plc_connections."""
        statement = select(PrivilegeModel).filter_by(deleted_at=None).options(selectinload(PrivilegeModel.routes))
        datatables = DataTables(session, PrivilegeModel, statement)
        return await datatables.process(request_data=request_data)
