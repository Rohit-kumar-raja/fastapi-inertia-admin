from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey
from ...common.models.base_model import BaseModel
from .user_model import UserRoleLinkModel,UserModel
if TYPE_CHECKING:
    from .route_model import RouteModel
    from .role_model import RolePermissionLinkModel



class RolePermissionLinkModel(BaseModel):
    """
    Association table for the Many-to-Many relationship between Permission and Role.
    """

    __tablename__ = "auth_route_role"

    auth_route_id: Mapped[str] = mapped_column(ForeignKey("auth_route.id"), primary_key=True)
    auth_role_id: Mapped[str] = mapped_column(ForeignKey("auth_role.id"), primary_key=True)


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
