"""
WebPushService — sends push notifications to subscribed browsers using VAPID.
"""
import json
import logging
from typing import List

from pywebpush import webpush, WebPushException

from ..models.push_subscription_model import PushSubscriptionModel
from ...config.settings import settings
from  ...common.uow.uow import AsyncUnitOfWork
from ..repositories.webpush_repository import WebPushRepository

logger = logging.getLogger(__name__)


class WebPushService:
    """Handles push subscription management and sending web push notifications via UoW."""
    def __init__(self, uow: AsyncUnitOfWork[WebPushRepository]):
        self.uow = uow

    async def subscribe(self, user_id: str, endpoint: str, p256dh: str, auth_key: str) -> PushSubscriptionModel:
        """Save or update a push subscription for a user."""
        existing = await self.uow.repo.get_by_endpoint(endpoint)

        if existing:
            existing.user_id = user_id
            existing.p256dh = p256dh
            existing.auth_key = auth_key
            await self.uow.repo.update(existing)
            return existing

        sub = PushSubscriptionModel(
            user_id=user_id,
            endpoint=endpoint,
            p256dh=p256dh,
            auth_key=auth_key,
        )
        await self.uow.repo.add(sub)
        return sub

    async def unsubscribe(self, endpoint: str) -> bool:
        """Remove a push subscription by endpoint."""
        rowcount = await self.uow.repo.delete_by_endpoint(endpoint)
        return rowcount > 0

    async def get_user_subscriptions(self, user_id: str) -> List[PushSubscriptionModel]:
        """Get all push subscriptions for a user."""
        return await self.uow.repo.get_user_subscriptions(user_id)

    @staticmethod
    def _send_push(subscription_info: dict, payload: dict) -> bool:
        """Send a single push notification. Returns True on success."""
        try:
            webpush(
                subscription_info=subscription_info,
                data=json.dumps(payload),
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={"sub": settings.VAPID_CLAIMS_EMAIL},
            )
            return True
        except WebPushException as e:
            logger.warning(f"WebPush failed: {e}")
            if hasattr(e, 'response') and e.response and e.response.status_code in (404, 410):
                return False
            return False
        except Exception as e:
            logger.error(f"WebPush unexpected error: {e}")
            return False

    async def send_to_user(self, user_id: str, title: str, message: str, notification_type: str, url: str = "/admin/dashboard") -> int:
        """Send push notification to all of a user's subscribed browsers."""
        subs = await self.get_user_subscriptions(user_id)
        if not subs:
            return 0

        payload = {
            "title": title,
            "body": message,
            "type": notification_type,
            "url": url,
        }

        success_count = 0
        dead_endpoints = []

        for sub in subs:
            subscription_info = {
                "endpoint": sub.endpoint,
                "keys": {"p256dh": sub.p256dh, "auth": sub.auth_key},
            }
            ok = self._send_push(subscription_info, payload)
            if ok:
                success_count += 1
            else:
                dead_endpoints.append(sub.endpoint)

        if dead_endpoints:
            for endpoint in dead_endpoints:
                await self.unsubscribe(endpoint)

        return success_count

    async def broadcast(self, title: str, message: str, notification_type: str, url: str = "/admin/dashboard") -> int:
        """Send push notification to ALL subscribed browsers."""
        all_subs = await self.uow.repo.get_all_active_subscriptions()

        if not all_subs:
            return 0

        payload = {
            "title": title,
            "body": message,
            "type": notification_type,
            "url": url,
        }

        success_count = 0
        dead_endpoints = []

        for sub in all_subs:
            subscription_info = {
                "endpoint": sub.endpoint,
                "keys": {"p256dh": sub.p256dh, "auth": sub.auth_key},
            }
            ok = self._send_push(subscription_info, payload)
            if ok:
                success_count += 1
            else:
                dead_endpoints.append(sub.endpoint)

        if dead_endpoints:
            for endpoint in dead_endpoints:
                await self.unsubscribe(endpoint)

        return success_count
