from fastapi import APIRouter
from .setting_router import setting_router
from .dashboard_router import dashboard_router

admin_router = APIRouter(prefix="/admin", tags=["Admin"])
admin_router.include_router(setting_router)
admin_router.include_router(dashboard_router)