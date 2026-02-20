from typing import Optional
from sqlalchemy import String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column
from .. import BaseModel


class AppSettingModel(BaseModel):
    """
    Generic key-value settings store.
    Each row is one setting: key -> value.
    Optionally grouped by `group` for logical organization.

    Examples:
        key="site_maintenance_mode", value="false", group="general"
        key="smtp_host", value="smtp.gmail.com", group="mail"
        key="default_pagination", value="25", group="general"
    """

    __tablename__ = "app_setting"

    key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    group: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default="general", index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    __table_args__ = (
        Index("ix_app_setting_group_key", "group", "key"),
    )
