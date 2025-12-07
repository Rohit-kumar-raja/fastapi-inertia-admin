from uuid import UUID
from pydantic import Field
from typing import List, Optional
from core.common.schemas import BaseSchema


class UserBaseSchema(BaseSchema):
    username: str = Field(max_length=150, description="Unique Username")


class UserSchema(UserBaseSchema):
    """
    UserSchema is used to validate user data.
    """

    password: str = Field(max_length=128, description="Hashed Password")
    role_ids: Optional[List[UUID]] = Field([], description="List of Role UUIDs")


class UserRestPasswordSchema(BaseSchema):
    """
    UserRestPasswordSchema is used to validate user reset password data.
    """

    password: str = Field(max_length=128, description="Hashed Password", min_length=8)
    confirm_password: str = Field(max_length=128, description="Hashed Password", min_length=8)
