# AppUser module — fastapi-users integration for forgot/reset password
from core.config import settings
from core.dependencies import get_db
from core.dependencies.inertia_dependency import InertiaDep

__all__ = ["get_db", "settings", "InertiaDep"]
