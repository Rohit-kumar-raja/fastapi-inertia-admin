from typing import List
from uuid import UUID
from pydantic import Field
from core.common.schemas import BaseSchema


class RoleSchema(BaseSchema):
    """
    RoleSchema is used to validate Role data.
    """

    name: str = Field(..., description="Name field")
    permission_ids: List[UUID] = Field([], description="List of Permission UUIDs")
