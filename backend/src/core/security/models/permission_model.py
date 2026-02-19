from typing import List, TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...common.models.base_model import BaseModel

if TYPE_CHECKING:
    from .role_model import RoleModel, RolePermissionLinkModel


class PermissionModel(BaseModel):
    """
    PermissionModel represents action-based permissions.
    Permissions are auto-synced from FastAPI route names (e.g. 'admin.role.read').
    """

    __tablename__ = "auth_permission"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    module: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Many-to-Many Relationship with RoleModel
    roles: Mapped[List["RoleModel"]] = relationship(
        back_populates="permissions", secondary="auth_role_permission", viewonly=True
    )
