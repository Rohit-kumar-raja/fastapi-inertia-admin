from typing import List
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.repository.base_repository import BaseRepository
from ..models.notification_model import NotificationModel


class NotificationRepository(BaseRepository[NotificationModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, NotificationModel)

    async def get_user_notifications(self, user_id: str, limit: int = 20) -> List[NotificationModel]:
        statement = (
            select(NotificationModel)
            .where(
                NotificationModel.user_id == user_id
            )
            .order_by(NotificationModel.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_unread_count(self, user_id: str) -> int:
        statement = select(func.count(NotificationModel.id)).where(
            NotificationModel.user_id == user_id,
            NotificationModel.is_read == False
        )
        result = await self.session.execute(statement)
        return result.scalar() or 0

    async def mark_as_read(self, notification_id: UUID, user_id: str) -> int:
        stmt = (
            update(NotificationModel)
            .where(
                NotificationModel.id == notification_id,
                NotificationModel.user_id == user_id,
            )
            .values(is_read=True)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def mark_all_read(self, user_id: str) -> int:
        stmt = (
            update(NotificationModel)
            .where(
                NotificationModel.user_id == user_id,
                NotificationModel.is_read == False
            )
            .values(is_read=True)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def delete_notification(self, notification_id: UUID, user_id: str) -> int:
        stmt = (
            update(NotificationModel)
            .where(
                NotificationModel.id == notification_id,
                NotificationModel.user_id == user_id,
            )
            .values(deleted_at=datetime.utcnow())
        )
        result = await self.session.execute(stmt)
        
        await self.session.flush()
        return result.rowcount
