from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.repository.base_repository import BaseRepository
from ..models.app_setting_model import AppSettingModel


class AppSettingRepository(BaseRepository[AppSettingModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AppSettingModel)

    async def get_all_settings(self, group: Optional[str] = None) -> List[AppSettingModel]:
        stmt = select(AppSettingModel).where(AppSettingModel.deleted_at.is_(None))
        if group:
            stmt = stmt.where(AppSettingModel.group == group)
        stmt = stmt.order_by(AppSettingModel.group, AppSettingModel.key)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_key(self, key: str) -> Optional[AppSettingModel]:
        result = await self.session.execute(
            select(AppSettingModel).where(
                AppSettingModel.key == key,
                AppSettingModel.deleted_at.is_(None),
            )
        )
        return result.scalars().first()
