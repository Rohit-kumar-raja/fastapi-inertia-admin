from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.notification_model import NotificationModel


class NotificationService:
    """
    NotificationService handles business logic for notifications.
    """

    @staticmethod
    async def get_user_notifications(
        user_id: str, session: AsyncSession, limit: int = 20
    ) -> List[NotificationModel]:
        """Fetch recent notifications for a user, newest first."""
        statement = (
            select(NotificationModel)
            .where(
                NotificationModel.user_id == user_id,
                NotificationModel.deleted_at.is_(None),
            )
            .order_by(NotificationModel.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_unread_count(user_id: str, session: AsyncSession) -> int:
        """Get the count of unread notifications."""
        statement = select(func.count(NotificationModel.id)).where(
            NotificationModel.user_id == user_id,
            NotificationModel.is_read == False,
            NotificationModel.deleted_at.is_(None),
        )
        result = await session.execute(statement)
        return result.scalar() or 0

    @staticmethod
    async def mark_as_read(
        notification_id: UUID, user_id: str, session: AsyncSession
    ) -> bool:
        """Mark a single notification as read."""
        stmt = (
            update(NotificationModel)
            .where(
                NotificationModel.id == notification_id,
                NotificationModel.user_id == user_id,
            )
            .values(is_read=True)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def mark_all_read(user_id: str, session: AsyncSession) -> int:
        """Mark all notifications as read for a user. Returns count updated."""
        stmt = (
            update(NotificationModel)
            .where(
                NotificationModel.user_id == user_id,
                NotificationModel.is_read == False,
                NotificationModel.deleted_at.is_(None),
            )
            .values(is_read=True)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount

    @staticmethod
    async def create_notification(
        user_id: str,
        title: str,
        message: str,
        type: str,
        session: AsyncSession,
    ) -> NotificationModel:
        """Create a new notification."""
        notification = NotificationModel(
            user_id=user_id,
            title=title,
            message=message or "",
            type=type,
        )
        session.add(notification)
        await session.commit()
        await session.refresh(notification)
        return notification

    @staticmethod
    async def delete_notification(
        notification_id: UUID, user_id: str, session: AsyncSession
    ) -> bool:
        """Delete (soft) a notification."""
        from datetime import datetime

        stmt = (
            update(NotificationModel)
            .where(
                NotificationModel.id == notification_id,
                NotificationModel.user_id == user_id,
            )
            .values(deleted_at=datetime.utcnow())
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def create_for_all_users(
        title: str,
        message: str,
        type: str,
        session: AsyncSession,
    ) -> int:
        """Create a notification for all active users (broadcast)."""
        from ..models.user_model import UserModel

        result = await session.execute(
            select(UserModel.id).where(UserModel.deleted_at.is_(None))
        )
        user_ids = result.scalars().all()
        count = 0
        for uid in user_ids:
            notification = NotificationModel(
                user_id=uid, title=title, message=message or "", type=type
            )
            session.add(notification)
            count += 1
        await session.commit()
        return count
