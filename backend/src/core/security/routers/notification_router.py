from uuid import UUID
from fastapi import APIRouter, Depends, Request, status
from pydantic import BaseModel

from ..services.notification_service import NotificationService
from ..repositories.notification_repository import NotificationRepository

from ..services.webpush_service import WebPushService
from ..repositories.webpush_repository import WebPushRepository

from ...dependencies.service_dependency import get_service

from ..utils import error_response, response
from ...config.settings import settings


notification_router = APIRouter(prefix="/notifications", tags=["notifications"])


# ─── Schemas ──────────────────────────────────────────────────────────────────
class CreateNotificationSchema(BaseModel):
    title: str
    message: str = ""
    type: str = "info"  # info | success | warning | error
    user_id: str | None = None  # None = self


class PushSubscriptionKeys(BaseModel):
    p256dh: str
    auth: str


class PushSubscribeSchema(BaseModel):
    endpoint: str
    keys: PushSubscriptionKeys


# ─── VAPID Public Key ────────────────────────────────────────────────────────
@notification_router.get("/vapid-public-key", status_code=status.HTTP_200_OK, name="admin.notification.vapid-key")
async def get_vapid_public_key():
    """Return the VAPID public key so the frontend can subscribe."""
    return response(
        data={"publicKey": settings.VAPID_PUBLIC_KEY},
        message="VAPID public key"
    )


# ─── Push Subscription ───────────────────────────────────────────────────────
@notification_router.post("/push/subscribe", status_code=status.HTTP_201_CREATED, name="admin.notification.push.subscribe")
async def push_subscribe(
    payload: PushSubscribeSchema,
    request: Request,
    push_service: WebPushService = Depends(get_service(WebPushService, WebPushRepository))
):
    """Save a browser push subscription for the current user."""
    user = request.state.user
    sub = await push_service.subscribe(
        user_id=user["id"],
        endpoint=payload.endpoint,
        p256dh=payload.keys.p256dh,
        auth_key=payload.keys.auth,
    )
    return response(data={"id": str(sub.id)}, message="Push subscription saved")


@notification_router.post("/push/unsubscribe", status_code=status.HTTP_200_OK, name="admin.notification.push.unsubscribe")
async def push_unsubscribe(
    payload: PushSubscribeSchema,
    push_service: WebPushService = Depends(get_service(WebPushService, WebPushRepository))
):
    """Remove a browser push subscription."""
    success = await push_service.unsubscribe(payload.endpoint)
    if not success:
        return error_response(message="Subscription not found", status_code=404)
    return response(data=None, message="Push subscription removed")


# ─── Notifications CRUD ──────────────────────────────────────────────────────
@notification_router.get("", status_code=status.HTTP_200_OK, name="admin.notification.list")
async def list_notifications(
    request: Request,
    notif_service: NotificationService = Depends(get_service(NotificationService, NotificationRepository))
):
    """Get current user's notifications."""
    user = request.state.user
    data = await notif_service.get_user_notifications(user["id"])
    return response(data=data, message="Notifications fetched")


@notification_router.get("/count", status_code=status.HTTP_200_OK, name="admin.notification.count")
async def unread_count(
    request: Request,
    notif_service: NotificationService = Depends(get_service(NotificationService, NotificationRepository))
):
    """Get unread notification count."""
    user = request.state.user
    count = await notif_service.get_unread_count(user["id"])
    return response(data={"count": count}, message="Unread count fetched")


@notification_router.put("/{notification_id}/read", status_code=status.HTTP_200_OK, name="admin.notification.read")
async def mark_read(
    notification_id: UUID, 
    request: Request,
    notif_service: NotificationService = Depends(get_service(NotificationService, NotificationRepository))
):
    """Mark a notification as read."""
    user = request.state.user
    success = await notif_service.mark_as_read(notification_id, user["id"])
    if not success:
        return error_response(message="Notification not found", status_code=404)
    return response(data=None, message="Marked as read")


@notification_router.put("/read-all", status_code=status.HTTP_200_OK, name="admin.notification.read-all")
async def mark_all_read(
    request: Request,
    notif_service: NotificationService = Depends(get_service(NotificationService, NotificationRepository))
):
    """Mark all notifications as read."""
    user = request.state.user
    count = await notif_service.mark_all_read(user["id"])
    return response(data={"count": count}, message=f"{count} notifications marked as read")


@notification_router.delete("/{notification_id}", status_code=status.HTTP_200_OK, name="admin.notification.delete")
async def delete_notification(
    notification_id: UUID, 
    request: Request,
    notif_service: NotificationService = Depends(get_service(NotificationService, NotificationRepository))
):
    """Delete a notification."""
    user = request.state.user
    success = await notif_service.delete_notification(notification_id, user["id"])
    if not success:
        return error_response(message="Notification not found", status_code=404)
    return response(data=None, message="Notification deleted")


@notification_router.post("", status_code=status.HTTP_201_CREATED, name="admin.notification.create")
async def create_notification(
    payload: CreateNotificationSchema, 
    request: Request,
    notif_service: NotificationService = Depends(get_service(NotificationService, NotificationRepository)),
    push_service: WebPushService = Depends(get_service(WebPushService, WebPushRepository))
):
    """Create a notification and send web push to the target user."""
    user = request.state.user
    target_user_id = payload.user_id or user["id"]

    data = await notif_service.create_notification(
        user_id=target_user_id,
        title=payload.title,
        message=payload.message,
        type=payload.type,
    )

    if settings.VAPID_PRIVATE_KEY:
        await push_service.send_to_user(
            user_id=target_user_id,
            title=payload.title,
            message=payload.message,
            notification_type=payload.type,
        )

    return response(data=data, message="Notification created")
