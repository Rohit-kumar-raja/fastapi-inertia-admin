from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.repository.base_repository import BaseRepository
from ..models.user_model import UserModel


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        statement = select(UserModel).where(UserModel.username == username, UserModel.deleted_at.is_(None))
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        statement = select(UserModel).where(UserModel.email == email, UserModel.deleted_at.is_(None))
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_all_active_users(self) -> List[UserModel]:
        statement = select(UserModel).where(UserModel.deleted_at.is_(None)).options(selectinload(UserModel.roles))
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_by_id_with_roles(self, uuid: str) -> Optional[UserModel]:
        statement = (
            select(UserModel)
            .where(UserModel.id == uuid, UserModel.deleted_at.is_(None))
            .options(selectinload(UserModel.roles))
        )
        result = await self.session.execute(statement)
        return result.scalars().first()
