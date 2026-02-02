# Configuration file

from ...core.config import settings
from ...core.common.models.base_model import BaseModel
from ...core.security.schemas.base_schema import APIResponseSchema
from ...core.dependencies import get_db,auth_dependency
from ...core.config.inertia import InertiaDep


__all__ = ["get_db", "settings", "BaseModel","APIResponseSchema","InertiaDep","auth_dependency"]
