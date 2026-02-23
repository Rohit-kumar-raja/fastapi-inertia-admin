from typing import List
from uuid import UUID

from ..models.notification_model import NotificationModel
from  ...common.uow.uow import AsyncUnitOfWork
from ..repositories.notification_repository import NotificationRepository
from ..repositories.user_repository import UserRepository


class NotificationService:
    """
    NotificationService handles business logic for notifications using UoW.
    """
    def __init__(self, uow: AsyncUnitOfWork[NotificationRepository]):
        self.uow = uow

    async def get_user_notifications(self, user_id: str, limit: int = 20) -> List[NotificationModel]:
        """Fetch recent notifications for a user, newest first."""
        return await self.uow.repo.get_user_notifications(user_id, limit)

    async def get_unread_count(self, user_id: str) -> int:
        """Get the count of unread notifications."""
        return await self.uow.repo.get_unread_count(user_id)

    async def mark_as_read(self, notification_id: UUID, user_id: str) -> bool:
        """Mark a single notification as read."""
        rowcount = await self.uow.repo.mark_as_read(notification_id, user_id)
        return rowcount > 0

    async def mark_all_read(self, user_id: str) -> int:
        """Mark all notifications as read for a user. Returns count updated."""
        return await self.uow.repo.mark_all_read(user_id)

    async def create_notification(self, user_id: str, title: str, message: str, type: str) -> NotificationModel:
        """Create a new notification."""
        notification = NotificationModel(
            user_id=user_id,
            title=title,
            message=message or "",
            type=type,
        )
        await self.uow.repo.add(notification)
        return notification

    async def delete_notification(self, notification_id: UUID, user_id: str) -> bool:
        """Delete (soft) a notification."""
        rowcount = await self.uow.repo.delete_notification(notification_id, user_id)
        return rowcount > 0

    async def create_for_all_users(self, title: str, message: str, type: str) -> int:
        """Create a notification for all active users (broadcast)."""
        user_repo = self.uow.get_repo(UserRepository)
        users = await user_repo.get_all_active_users()
        count = 0
        for u in users:
            notification = NotificationModel(
                user_id=str(u.id), title=title, message=message or "", type=type
            )
            self.uow.session.add(notification)
            count += 1
        return count
