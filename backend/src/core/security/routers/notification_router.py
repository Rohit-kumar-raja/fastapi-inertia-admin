from uuid import UUID
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from ..services.notification_service import NotificationService
from ..utils import error_response, response
from .. import get_db


notification_router = APIRouter(prefix="/notifications", tags=["notifications"])


class CreateNotificationSchema(BaseModel):
    title: str
    message: str = ""
    type: str = "info"  # info | success | warning | error
    user_id: str | None = None  # None = self


@notification_router.get("", status_code=status.HTTP_200_OK, name="admin.notification.list")
async def list_notifications(request: Request, session: AsyncSession = Depends(get_db)):
    """Get current user's notifications."""
    user = request.state.user
    data = await NotificationService.get_user_notifications(user["id"], session)
    return response(data=data, message="Notifications fetched")


@notification_router.get("/count", status_code=status.HTTP_200_OK, name="admin.notification.count")
async def unread_count(request: Request, session: AsyncSession = Depends(get_db)):
    """Get unread notification count."""
    user = request.state.user
    count = await NotificationService.get_unread_count(user["id"], session)
    return response(data={"count": count}, message="Unread count fetched")


@notification_router.put("/{notification_id}/read", status_code=status.HTTP_200_OK, name="admin.notification.read")
async def mark_read(notification_id: UUID, request: Request, session: AsyncSession = Depends(get_db)):
    """Mark a notification as read."""
    user = request.state.user
    success = await NotificationService.mark_as_read(notification_id, user["id"], session)
    if not success:
        return error_response(message="Notification not found", status_code=404)
    return response(data=None, message="Marked as read")


@notification_router.put("/read-all", status_code=status.HTTP_200_OK, name="admin.notification.read-all")
async def mark_all_read(request: Request, session: AsyncSession = Depends(get_db)):
    """Mark all notifications as read."""
    user = request.state.user
    count = await NotificationService.mark_all_read(user["id"], session)
    return response(data={"count": count}, message=f"{count} notifications marked as read")


@notification_router.delete("/{notification_id}", status_code=status.HTTP_200_OK, name="admin.notification.delete")
async def delete_notification(notification_id: UUID, request: Request, session: AsyncSession = Depends(get_db)):
    """Delete a notification."""
    user = request.state.user
    success = await NotificationService.delete_notification(notification_id, user["id"], session)
    if not success:
        return error_response(message="Notification not found", status_code=404)
    return response(data=None, message="Notification deleted")


@notification_router.post("", status_code=status.HTTP_201_CREATED, name="admin.notification.create")
async def create_notification(payload: CreateNotificationSchema, request: Request, session: AsyncSession = Depends(get_db)):
    """Create a notification (for testing or system use)."""
    user = request.state.user
    target_user_id = payload.user_id or user["id"]
    data = await NotificationService.create_notification(
        user_id=target_user_id,
        title=payload.title,
        message=payload.message,
        type=payload.type,
        session=session,
    )
    return response(data=data, message="Notification created")
