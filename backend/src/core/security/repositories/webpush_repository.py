from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.repository.base_repository import BaseRepository
from ..models.push_subscription_model import PushSubscriptionModel


class WebPushRepository(BaseRepository[PushSubscriptionModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PushSubscriptionModel)

    async def get_by_endpoint(self, endpoint: str) -> Optional[PushSubscriptionModel]:
        stmt = select(PushSubscriptionModel).where(PushSubscriptionModel.endpoint == endpoint)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_by_endpoint(self, endpoint: str) -> int:
        stmt = delete(PushSubscriptionModel).where(PushSubscriptionModel.endpoint == endpoint)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def get_user_subscriptions(self, user_id: str) -> List[PushSubscriptionModel]:
        stmt = select(PushSubscriptionModel).where(
            PushSubscriptionModel.user_id == user_id,
            PushSubscriptionModel.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_active_subscriptions(self) -> List[PushSubscriptionModel]:
        stmt = select(PushSubscriptionModel).where(PushSubscriptionModel.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalars().all()
