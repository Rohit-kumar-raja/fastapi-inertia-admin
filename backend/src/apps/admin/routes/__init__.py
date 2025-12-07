from fastapi import APIRouter
from .setting_router import setting_router

admin_router = APIRouter()
admin_router.include_router(setting_router)