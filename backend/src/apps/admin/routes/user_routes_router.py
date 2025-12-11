from fastapi import APIRouter, Depends
from src.core.config.inertia import InertiaDep
from inertia import InertiaResponse

user_routes_router = APIRouter(prefix="/admin/users", tags=["admin-users-routes"])


@user_routes_router.get("", response_model=None)
async def users_index(inertia: InertiaDep) -> InertiaResponse:
    """Users management index page"""
    return await inertia.render("Admin/Users/Index")


@user_routes_router.get("/create", response_model=None)
async def users_create(inertia: InertiaDep) -> InertiaResponse:
    """User creation page"""
    return await inertia.render("Admin/Users/Create")


@user_routes_router.get("/{user_id}/edit", response_model=None)
async def users_edit(user_id: str, inertia: InertiaDep) -> InertiaResponse:
    """User edit page"""
    return await inertia.render("Admin/Users/Edit", {"userId": user_id})
