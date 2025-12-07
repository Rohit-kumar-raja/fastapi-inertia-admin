from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .user_role_link_model import UserRoleLinkModel
from .role_permission_link_model import RolePermissionLinkModel
from .base_model import BaseModel

if TYPE_CHECKING:
    from .route_model import RouteModel
    from .user_model import UserModel


class RoleModel(BaseModel):
    """
    RoleModel represents the schema for auth_role.
    """

    __tablename__ = "auth_role"

    name: Mapped[str] = mapped_column(String, nullable=False)

    # Many-to-Many Relationship with RouteModel
    routes: Mapped[List["RouteModel"]] = relationship(
        back_populates="roles", secondary=RolePermissionLinkModel.__table__
    )

    users: Mapped[List["UserModel"]] = relationship(back_populates="roles", secondary=UserRoleLinkModel.__table__)
