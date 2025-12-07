from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import BaseModel


class RolePermissionLinkModel(BaseModel):
    """
    Association table for the Many-to-Many relationship between Permission and Role.
    """

    __tablename__ = "auth_route_role"

    auth_route_id: Mapped[str] = mapped_column(ForeignKey("auth_route.id"), primary_key=True)
    auth_role_id: Mapped[str] = mapped_column(ForeignKey("auth_role.id"), primary_key=True)
