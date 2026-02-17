from fastapi import APIRouter,Depends
from .. import InertiaDep,web_auth

setting_router = APIRouter(dependencies=[Depends(web_auth)])


@setting_router.get("/settings")
async def settings(inertia: InertiaDep):
    return await inertia.render("Dashboard")
