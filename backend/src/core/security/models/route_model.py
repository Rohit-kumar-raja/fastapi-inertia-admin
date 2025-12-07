from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .role_model import RoleModel
from .role_permission_link_model import RolePermissionLinkModel
from .privilege_permission_link_model import PrivilegeRouteLinkModel
from .base_model import BaseModel

if TYPE_CHECKING:
    from .privilege_model import PrivilegeModel


class RouteModel(BaseModel):
    """
    RouteModel represents the schema for auth_route.
    """

    __tablename__ = "auth_route"

    name: Mapped[str] = mapped_column(String, nullable=False)
    icon: Mapped[str] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(default=0)
    path_name: Mapped[str] = mapped_column(String, nullable=True)
    component: Mapped[str] = mapped_column(String, nullable=True)
    parent_id: Mapped[Optional[str]] = mapped_column(ForeignKey("auth_route.id"), nullable=True)

    children: Mapped[List["RouteModel"]] = relationship(
        back_populates="parent", lazy="joined", order_by="RouteModel.order"
    )
    parent: Mapped[Optional["RouteModel"]] = relationship(back_populates="children", remote_side="RouteModel.id")

    roles: Mapped[List[RoleModel]] = relationship(back_populates="routes", secondary=RolePermissionLinkModel.__table__)
    privileges: Mapped[List["PrivilegeModel"]] = relationship(
        back_populates="routes", secondary=PrivilegeRouteLinkModel.__table__
    )

    # def __str__(self):
    #     return f"{{'name': '{self.name}' }}"
