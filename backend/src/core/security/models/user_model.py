from typing import List, Optional,TYPE_CHECKING
from sqlalchemy import String, Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...common.models.base_model import BaseModel

if TYPE_CHECKING:
    from .role_model import RoleModel



class UserRoleLinkModel(BaseModel):
    """
    Association table for the Many-to-Many relationship between User and Role.
    """

    __tablename__ = "security_user_roles"

    security_user_id: Mapped[str] = mapped_column(ForeignKey("security_user.id"), primary_key=True)
    security_role_id: Mapped[str] = mapped_column(ForeignKey("security_role.id"), primary_key=True)



class UserModel(BaseModel):
    """
    UserModel represents the schema for security_user.
    """

    __tablename__ = "security_user"

    username: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    avatar: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Many-to-Many Relationship with RoleModel
    roles: Mapped[List["RoleModel"]] = relationship(back_populates="users", secondary=UserRoleLinkModel.__table__)

