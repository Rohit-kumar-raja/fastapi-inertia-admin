from fastapi import APIRouter
from .setting_router import setting_router
from .user_routes_router import user_routes_router
from .role_routes_router import role_routes_router
from .dashboard_router import dashboard_router

admin_router = APIRouter(prefix="/admin", tags=["Admin"])
admin_router.include_router(setting_router)
admin_router.include_router(user_routes_router)
admin_router.include_router(role_routes_router)
admin_router.include_router(dashboard_router)