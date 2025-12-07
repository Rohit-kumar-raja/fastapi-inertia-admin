from fastapi import APIRouter
from .. import InertiaDep

setting_router = APIRouter()


@setting_router.get("/settings")
async def settings(inertia: InertiaDep):
    return await inertia.render("Dashboard")
