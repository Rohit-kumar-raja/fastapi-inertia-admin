"""
AppUser model — completely independent from security_user.
This is the user table for the mobile application.
Uses fastapi-users' SQLAlchemyBaseUserTableUUID for built-in auth fields.
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from core.config.database import Base


class AppUserModel(SQLAlchemyBaseUserTableUUID, Base):
    """
    Mobile application user.
    Inherits email, hashed_password, is_active, is_superuser, is_verified from fastapi-users.
    """

    __tablename__ = "appuser_user"

    # Additional fields specific to mobile app users
    first_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
