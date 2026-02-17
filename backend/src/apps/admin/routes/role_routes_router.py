from fastapi import APIRouter, Depends
from .. import InertiaDep
from inertia import InertiaResponse

role_routes_router = APIRouter(prefix="/admin/roles", tags=["admin-roles-routes"])


@role_routes_router.get("", response_model=None)
async def roles_index(inertia: InertiaDep) -> InertiaResponse:
    """Roles management index page"""
    return await inertia.render("Admin/Roles/Index")


@role_routes_router.get("/create", response_model=None)
async def roles_create(inertia: InertiaDep) -> InertiaResponse:
    """Role creation page"""
    return await inertia.render("Admin/Roles/Create")


@role_routes_router.get("/{role_id}/edit", response_model=None)
async def roles_edit(role_id: str, inertia: InertiaDep) -> InertiaResponse:
    """Role edit page"""
    return await inertia.render("Admin/Roles/Edit", {"roleId": role_id})
