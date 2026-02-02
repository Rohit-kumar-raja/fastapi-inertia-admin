from fastapi import APIRouter,Depends
from .. import InertiaDep,auth_dependency

setting_router = APIRouter(dependencies=[Depends(auth_dependency.auth)])


@setting_router.get("/settings")
async def settings(inertia: InertiaDep):
    return await inertia.render("Dashboard")
