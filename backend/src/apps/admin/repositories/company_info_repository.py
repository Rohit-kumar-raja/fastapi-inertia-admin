from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.repository.base_repository import BaseRepository
from ..models.company_info_model import CompanyInfoModel


class CompanyInfoRepository(BaseRepository[CompanyInfoModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CompanyInfoModel)

    async def get_company_info(self) -> Optional[CompanyInfoModel]:
        result = await self.session.execute(
            select(CompanyInfoModel).limit(1)
        )
        return result.scalars().first()
