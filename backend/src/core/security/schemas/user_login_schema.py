from typing import List
from uuid import UUID
from pydantic import BaseModel, Field
from ...common.schemas import BaseSchema


class UserLoginSchema(BaseSchema):
    """
    User_loginSchema is used to validate user_login data.
    """

    username: str = Field(
        ...,
        description="Name field",
    )
    password: str = Field(..., description="Password field", min_length=8)


class UserDetailsResponseSchema(BaseSchema):
    """
    UserDetailsResponseSchema is used to validate user_login response data.
    """

    id: UUID
    username: str = Field(..., alias="name", description="Name field")


class UserLoginResponseSchema(BaseModel):
    """
    UserLoginResponseSchema is used to validate user_login response data.
    """

    user: UserDetailsResponseSchema
    permissions: List[str] = Field(default=[], description="List of user permission names")
