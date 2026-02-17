from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.role_schema import RoleSchema
from ..services.role_service import RoleService
from ..utils import error_response, response
from .. import get_db,InertiaDep
from datatables import DataTablesRequest

role_router = APIRouter(prefix="/roles", tags=["roles"])


@role_router.get("", status_code=status.HTTP_200_OK, name="admin.role.read")
async def index(inertia: InertiaDep):
    """Get all the data"""
    return await inertia.render("Admin/Roles/Index")


@role_router.post("", status_code=status.HTTP_201_CREATED, name="admin.role.write")
async def create(role: RoleSchema, session: AsyncSession = Depends(get_db), satatus_code=status.HTTP_201_CREATED):
    """Create new data based on the request."""
    is_unique = await RoleService.is_unique(name=role.name, session=session)
    if is_unique:
        return error_response(message="Role name already exists", status_code=422)

    response_data = await RoleService().create(role.model_dump(), session)
    return response(data=response_data, message="Data created successfully")


@role_router.get("/{uuid}", status_code=status.HTTP_200_OK, name="admin.role.read")
async def edit(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Read or edit the data based on the given UUID."""
    data = await RoleService().get_by_id(uuid, session)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")


@role_router.put("/{uuid}", status_code=status.HTTP_200_OK, name="admin.role.edit")
async def update(role: RoleSchema, uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Update the data based on the given UUID."""
    data = await RoleService().update(uuid, role.model_dump(), session)
    return response(data=data, message="Data updated successfully")


@role_router.delete("/{uuid}", status_code=status.HTTP_200_OK, name="admin.role.delete")
async def destroy(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Delete the data based on the given UUID."""
    data = await RoleService().delete(uuid, session)
    if not data:
        error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data deleted successfully")


@role_router.post("/filter", status_code=status.HTTP_200_OK, name="admin.role.datatables")
async def filter(request_data: DataTablesRequest, session: AsyncSession = Depends(get_db)):
    """Get all"""
    data = await RoleService().datatables(session, request_data)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")
