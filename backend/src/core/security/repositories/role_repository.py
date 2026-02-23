from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.repository.base_repository import BaseRepository
from ..models.role_model import RoleModel


class RoleRepository(BaseRepository[RoleModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RoleModel)

    async def get_by_name(self, name: str) -> Optional[RoleModel]:
        statement = select(RoleModel).where(RoleModel.name == name)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_roles_by_ids(self, role_ids: list[str]) -> List[RoleModel]:
        statement = select(RoleModel).where(RoleModel.id.in_(role_ids))
        result = await self.session.execute(statement)
        return result.unique().scalars().all()

    async def get_all_with_permissions(self) -> List[RoleModel]:
        statement = select(RoleModel).options(selectinload(RoleModel.permissions))
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_by_id_with_permissions(self, uuid: str) -> Optional[RoleModel]:
        statement = (
            select(RoleModel)
            .where(RoleModel.id == uuid)
            .options(selectinload(RoleModel.permissions))
        )
        result = await self.session.execute(statement)
        return result.scalars().first()
