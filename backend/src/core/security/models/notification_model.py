from typing import Optional
from sqlalchemy import String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from ...common.models.base_model import BaseModel


class NotificationModel(BaseModel):
    """
    NotificationModel represents admin notifications.
    """

    __tablename__ = "security_notification"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="info")  # info, success, warning, error
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
