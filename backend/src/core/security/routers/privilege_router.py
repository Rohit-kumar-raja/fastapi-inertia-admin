from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.privilege_schema import PrivilegeSchema
from ..utils import error_response, response
from ..services.privilege_service import PrivilegeService
from .. import get_db
from core.datatables import DataTablesRequest

privilege_router = APIRouter(prefix="/privileges", tags=["privileges"])


@privilege_router.get("", status_code=status.HTTP_200_OK, name="admin.privilege.read")
async def index(session: AsyncSession = Depends(get_db)):
    """Get all the data"""
    data = await PrivilegeService().get_all(session)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")


@privilege_router.post("", status_code=status.HTTP_201_CREATED, name="admin.privilege.write")
async def create(privilege: PrivilegeSchema, session: AsyncSession = Depends(get_db)):
    """Create new data based on the request."""
    is_unique = await PrivilegeService.is_unique(privilege.access, session)
    if is_unique:
        return error_response(message="Privilege name already exists", status_code=422)
    response_data = await PrivilegeService().create(privilege.model_dump(), session)
    return response(data=response_data, message="Data created successfully")


@privilege_router.get("/{uuid}", status_code=status.HTTP_200_OK, name="admin.privilege.read")
async def edit(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Read or edit the data based on the given UUID."""
    data = await PrivilegeService.get_by_id(uuid, session)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")


@privilege_router.put("/{uuid}", status_code=status.HTTP_200_OK, name="admin.privilege.edit")
async def update(privilege: PrivilegeSchema, uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Update the data based on the given UUID."""
    data = await PrivilegeService().update(uuid, privilege.model_dump(), session)
    return response(data=data, message="Data updated successfully")


@privilege_router.delete("/{uuid}", status_code=status.HTTP_200_OK, name="admin.privilege.delete")
async def destroy(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Delete the data based on the given UUID."""
    data = await PrivilegeService().delete(uuid, session)
    if data:
        return response(data=data, message="Data deleted successfully")
    else:
        return error_response(message="Data not found", status_code=404)


@privilege_router.post("/filter", status_code=status.HTTP_200_OK, name="admin.privilege.datatables")
async def filter(request_data: DataTablesRequest, session: AsyncSession = Depends(get_db)):
    """Get all"""
    data = await PrivilegeService().datatables(session, request_data)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")
