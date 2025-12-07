from typing import Generic, List, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.base_model import Base
from datetime import datetime
from core.datatables import DataTables, DataTablesRequest


T = TypeVar("T", bound=Base)


class BaseService(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def create(self, session: AsyncSession, data: dict) -> T:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one()

    async def get_all(self, session: AsyncSession) -> List[T]:
        result = await session.execute(select(self.model).where(self.model.deleted_at.is_(None)))
        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, obj_id: UUID) -> Optional[T]:
        result = await session.execute(select(self.model).where(self.model.id == obj_id))
        return result.scalar_one_or_none()

    async def update(self, session: AsyncSession, obj_id: UUID, data: dict) -> Optional[T]:
        stmt = update(self.model).where(self.model.id == obj_id).values(**data).returning(self.model)
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one_or_none()

    async def soft_delete(self, session: AsyncSession, obj_id: UUID) -> bool:
        instance = await session.get(self.model, obj_id)
        if instance and instance.deleted_at is None:
            instance.deleted_at = datetime.now()
            await session.commit()
            return True
        return False

    async def datatables(self, session: AsyncSession, request_data: DataTablesRequest) -> Optional[T]:
        statement = select(self.model).filter_by(deleted_at=None)
        datatables = DataTables(session, self.model, statement)
        return await datatables.process(request_data=request_data)
