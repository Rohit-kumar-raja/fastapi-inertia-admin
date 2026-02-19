from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from ...common.models.base_model import BaseModel


class PushSubscriptionModel(BaseModel):
    """
    Stores browser push subscription data for Web Push notifications.
    Each subscription corresponds to one browser on one device for one user.
    """

    __tablename__ = "auth_push_subscription"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("auth_user.id"), nullable=False)
    endpoint: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    p256dh: Mapped[str] = mapped_column(String(255), nullable=False)
    auth_key: Mapped[str] = mapped_column(String(255), nullable=False)
