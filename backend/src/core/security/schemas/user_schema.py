from uuid import UUID
from pydantic import Field, EmailStr
from typing import List, Optional
from ...common.schemas import BaseSchema


class UserBaseSchema(BaseSchema):
    username: str = Field(max_length=150, description="Unique Username")
    email: EmailStr = Field(description="User Email Address")
    phone: Optional[str] = Field(None, max_length=20, description="Phone Number")
    is_superuser: bool = Field(default=False, description="Superuser Flag")


class UserSchema(UserBaseSchema):
    """
    UserSchema is used to validate user data.
    """

    password: str = Field(min_length=8, max_length=128, description="User Password")
    role_ids: Optional[List[UUID]] = Field(default=[], description="List of Role UUIDs")


class UserRestPasswordSchema(BaseSchema):
    """
    UserRestPasswordSchema is used to validate user reset password data.
    """

    password: str = Field(max_length=128, description="Hashed Password", min_length=8)
    confirm_password: str = Field(max_length=128, description="Hashed Password", min_length=8)
