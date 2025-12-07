from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .privilege_permission_link_model import PrivilegeRouteLinkModel
from .route_model import RouteModel
from .base_model import BaseModel


class PrivilegeModel(BaseModel):
    """
    PrivilegeModel represents the schema for auth_privilege.
    """

    __tablename__ = "auth_privilege"

    access: Mapped[str] = mapped_column(String, nullable=False)

    routes: Mapped[List["RouteModel"]] = relationship(
        back_populates="privileges", secondary=PrivilegeRouteLinkModel.__table__
    )
