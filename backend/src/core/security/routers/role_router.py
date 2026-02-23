from uuid import UUID
from fastapi import APIRouter, Depends, status

from ..schemas.role_schema import RoleSchema
from ..services.role_service import RoleService
from ..repositories.role_repository import RoleRepository
from ...dependencies.service_dependency import get_service

from ..utils import error_response, response
from .. import InertiaDep
from ...dependencies.permission_dependency import require_permission
from datatables import DataTablesRequest

role_router = APIRouter(prefix="/administration/roles", tags=["roles"])


@role_router.get("", status_code=status.HTTP_200_OK, name="admin.role.read")
async def index(inertia: InertiaDep):
    """Get all the data"""
    return await inertia.render("Admin/Roles/Index")


@role_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    name="admin.role.write",
    dependencies=[Depends(require_permission("admin.role.write"))],
)
async def create(
    role: RoleSchema, 
    role_service: RoleService = Depends(get_service(RoleService, RoleRepository))
):
    """Create new data based on the request."""
    is_unique = await role_service.is_unique(name=role.name)
    if is_unique:
        return error_response(message="Role name already exists", status_code=422)

    response_data = await role_service.create(role.model_dump())
    return response(data=response_data, message="Data created successfully")


@role_router.get("/list", status_code=status.HTTP_200_OK, name="admin.role.list")
async def list_roles(
    role_service: RoleService = Depends(get_service(RoleService, RoleRepository))
):
    """Get all roles as JSON (for dropdowns/multiselects)."""
    data = await role_service.get_all()
    return response(data=data, message="Roles fetched successfully")


@role_router.get("/{uuid}", status_code=status.HTTP_200_OK, name="admin.role.detail")
async def edit(
    uuid: UUID,
    role_service: RoleService = Depends(get_service(RoleService, RoleRepository))
):
    """Read or edit the data based on the given UUID."""
    data = await role_service.get_by_id(uuid)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")


@role_router.put(
    "/{uuid}",
    status_code=status.HTTP_200_OK,
    name="admin.role.edit",
    dependencies=[Depends(require_permission("admin.role.edit"))],
)
async def update(
    role: RoleSchema,
    uuid: UUID,
    role_service: RoleService = Depends(get_service(RoleService, RoleRepository))
):
    """Update the data based on the given UUID."""
    data = await role_service.update(uuid, role.model_dump())
    return response(data=data, message="Data updated successfully")


@role_router.delete(
    "/{uuid}",
    status_code=status.HTTP_200_OK,
    name="admin.role.delete",
    dependencies=[Depends(require_permission("admin.role.delete"))],
)
async def destroy(
    uuid: UUID,
    role_service: RoleService = Depends(get_service(RoleService, RoleRepository))
):
    """Delete the data based on the given UUID."""
    data = await role_service.delete(uuid)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data deleted successfully")


@role_router.post("/filter", status_code=status.HTTP_200_OK, name="admin.role.datatables")
async def filter(
    request_data: DataTablesRequest,
    role_service: RoleService = Depends(get_service(RoleService, RoleRepository))
):
    """Get all"""
    data = await role_service.datatables(request_data)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")
