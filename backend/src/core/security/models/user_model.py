from typing import List, Optional
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user_role_link_model import UserRoleLinkModel
from .base_model import BaseModel
from .role_model import RoleModel


class UserModel(BaseModel):
    """
    UserModel represents the schema for auth_user.
    """

    __tablename__ = "auth_user"

    username: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Many-to-Many Relationship with RoleModel
    roles: Mapped[List["RoleModel"]] = relationship(back_populates="users", secondary=UserRoleLinkModel.__table__)
