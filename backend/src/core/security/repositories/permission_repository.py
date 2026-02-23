from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.repository.base_repository import BaseRepository
from ..models.permission_model import PermissionModel


class PermissionRepository(BaseRepository[PermissionModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PermissionModel)

    async def get_permissions_by_ids(self, permission_ids: list[str]) -> List[PermissionModel]:
        statement = select(PermissionModel).where(PermissionModel.id.in_(permission_ids))
        result = await self.session.execute(statement)
        return result.unique().scalars().all()

    async def get_all_active(self) -> List[PermissionModel]:
        statement = select(PermissionModel).where(PermissionModel.deleted_at.is_(None))
        result = await self.session.execute(statement)
        return result.scalars().all()
