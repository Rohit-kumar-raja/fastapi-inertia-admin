from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import BaseModel


class UserRoleLinkModel(BaseModel):
    """
    Association table for the Many-to-Many relationship between User and Role.
    """

    __tablename__ = "auth_user_roles"

    auth_user_id: Mapped[str] = mapped_column(ForeignKey("auth_user.id"), primary_key=True)
    auth_role_id: Mapped[str] = mapped_column(ForeignKey("auth_role.id"), primary_key=True)
