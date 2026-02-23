from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey
from ...common.models.base_model import BaseModel
from .user_model import UserRoleLinkModel, UserModel

if TYPE_CHECKING:
    from .permission_model import PermissionModel


class RolePermissionLinkModel(BaseModel):
    """
    Association table for the Many-to-Many relationship between Role and Permission.
    """

    __tablename__ = "security_role_permission"

    security_permission_id: Mapped[str] = mapped_column(ForeignKey("security_permission.id"), primary_key=True)
    security_role_id: Mapped[str] = mapped_column(ForeignKey("security_role.id"), primary_key=True)


class RoleModel(BaseModel):
    """
    RoleModel represents the schema for security_role.
    """

    __tablename__ = "security_role"

    name: Mapped[str] = mapped_column(String, nullable=False)

    # Many-to-Many Relationship with PermissionModel
    permissions: Mapped[List["PermissionModel"]] = relationship(
        back_populates="roles", secondary=RolePermissionLinkModel.__table__
    )

    users: Mapped[List["UserModel"]] = relationship(back_populates="roles", secondary=UserRoleLinkModel.__table__)
