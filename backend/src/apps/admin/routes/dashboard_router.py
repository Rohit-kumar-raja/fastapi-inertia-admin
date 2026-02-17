from fastapi import APIRouter
from .. import InertiaDep
from inertia import InertiaResponse

dashboard_router = APIRouter(prefix="/admin/dashboard", tags=["admin-dashboard-routes"])

@dashboard_router.get("", response_model=None)
async def dashboard_index(inertia: InertiaDep) -> InertiaResponse:
    """Admin Dashboard"""
    return await inertia.render("Admin/Dashboard")
