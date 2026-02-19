from typing import List, Optional
from uuid import UUID
from pydantic import Field
from ...common.schemas import BaseSchema


class PermissionSchema(BaseSchema):
    """
    PermissionSchema is used to validate Permission data.
    """

    name: str = Field(..., min_length=1, max_length=255, description="Permission name (e.g. 'admin.user.read')")
    module: str = Field(..., min_length=1, max_length=100, description="Module group (e.g. 'user')")
    description: Optional[str] = Field(None, description="Human-readable description")


class PermissionGroupSchema(BaseSchema):
    """
    Schema for grouped permissions response.
    """

    module: str
    permissions: List[PermissionSchema]
