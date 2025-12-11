from uuid import UUID
from pydantic import Field
from .privilege_schema import PrivilegeSchema
from ...common.schemas import BaseSchema


class RouteSchema(BaseSchema):
    """
    RouteSchema is used to validate Permission data.
    """

    name: str = Field(..., min_length=1, max_length=100, description="Name field")
    parent_id: UUID = Field(None, description="Parent id of the auth_route table")
    privilege_ids: list[UUID] = Field([], description="List of privilege ids")


class RouteResponseSchema(BaseSchema):
    """
    RouteResponseSchema is used to validate Permission response data.
    """

    id: UUID
    name: str = Field(..., min_length=1, max_length=100, description="Name field")
    path_name: str | None = Field(..., description="Path name field")
    component: str | None = Field(..., description="Component field")
    privileges: list[PrivilegeSchema] = Field([], description="List of privilege ids")
