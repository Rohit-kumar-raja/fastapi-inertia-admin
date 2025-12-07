from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import BaseModel


class PrivilegeRouteLinkModel(BaseModel):
    """
    PrivilegeRouteLinkModel represents the schema for auth_privilege_route.
    """

    __tablename__ = "auth_privilege_route"

    auth_privilege_id: Mapped[str] = mapped_column(ForeignKey("auth_privilege.id"), primary_key=True)
    auth_route_id: Mapped[str] = mapped_column(ForeignKey("auth_route.id"), primary_key=True)
