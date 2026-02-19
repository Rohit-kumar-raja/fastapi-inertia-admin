"""
WebPushService — sends push notifications to subscribed browsers using VAPID.
"""
import json
import logging
from typing import List, Optional
from uuid import UUID

from pywebpush import webpush, WebPushException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.push_subscription_model import PushSubscriptionModel
from ...config.settings import settings

logger = logging.getLogger(__name__)


class WebPushService:
    """Handles push subscription management and sending web push notifications."""

    @staticmethod
    async def subscribe(
        user_id: str,
        endpoint: str,
        p256dh: str,
        auth_key: str,
        session: AsyncSession,
    ) -> PushSubscriptionModel:
        """Save or update a push subscription for a user."""
        # Check if this endpoint already exists
        stmt = select(PushSubscriptionModel).where(
            PushSubscriptionModel.endpoint == endpoint
        )
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            # Update user_id and keys if the endpoint already exists
            existing.user_id = user_id
            existing.p256dh = p256dh
            existing.auth_key = auth_key
            await session.commit()
            await session.refresh(existing)
            return existing

        sub = PushSubscriptionModel(
            user_id=user_id,
            endpoint=endpoint,
            p256dh=p256dh,
            auth_key=auth_key,
        )
        session.add(sub)
        await session.commit()
        await session.refresh(sub)
        return sub

    @staticmethod
    async def unsubscribe(endpoint: str, session: AsyncSession) -> bool:
        """Remove a push subscription by endpoint."""
        stmt = delete(PushSubscriptionModel).where(
            PushSubscriptionModel.endpoint == endpoint
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def get_user_subscriptions(
        user_id: str, session: AsyncSession
    ) -> List[PushSubscriptionModel]:
        """Get all push subscriptions for a user."""
        stmt = select(PushSubscriptionModel).where(
            PushSubscriptionModel.user_id == user_id,
            PushSubscriptionModel.deleted_at.is_(None),
        )
        result = await session.execute(stmt)
        return result.scalars().all()

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
            # If subscription is expired/invalid (410 Gone or 404), return False
            if hasattr(e, 'response') and e.response and e.response.status_code in (404, 410):
                return False
            return False
        except Exception as e:
            logger.error(f"WebPush unexpected error: {e}")
            return False

    @staticmethod
    async def send_to_user(
        user_id: str,
        title: str,
        message: str,
        notification_type: str,
        session: AsyncSession,
        url: str = "/admin/dashboard",
    ) -> int:
        """Send push notification to all of a user's subscribed browsers.
        Returns the number of successful sends. Cleans up dead subscriptions."""
        subs = await WebPushService.get_user_subscriptions(user_id, session)
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
            ok = WebPushService._send_push(subscription_info, payload)
            if ok:
                success_count += 1
            else:
                dead_endpoints.append(sub.endpoint)

        # Clean up dead subscriptions
        if dead_endpoints:
            for endpoint in dead_endpoints:
                await WebPushService.unsubscribe(endpoint, session)

        return success_count

    @staticmethod
    async def broadcast(
        title: str,
        message: str,
        notification_type: str,
        session: AsyncSession,
        url: str = "/admin/dashboard",
    ) -> int:
        """Send push notification to ALL subscribed browsers. Returns total successful sends."""
        stmt = select(PushSubscriptionModel).where(
            PushSubscriptionModel.deleted_at.is_(None)
        )
        result = await session.execute(stmt)
        all_subs = result.scalars().all()

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
            ok = WebPushService._send_push(subscription_info, payload)
            if ok:
                success_count += 1
            else:
                dead_endpoints.append(sub.endpoint)

        if dead_endpoints:
            for endpoint in dead_endpoints:
                await WebPushService.unsubscribe(endpoint, session)

        return success_count
