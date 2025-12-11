from pydantic import Field
from ...common.schemas import BaseSchema


class PrivilegeSchema(BaseSchema):
    """
    PrivilegeSchema is used to validate privilege data.
    """

    access: str = Field(..., min_length=1, description="Access field")
