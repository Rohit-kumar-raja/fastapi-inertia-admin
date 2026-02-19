from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.permission_service import PermissionService
from ..utils import response, error_response
from .. import get_db, InertiaDep


permission_router = APIRouter(prefix="/administration/permissions", tags=["permissions"])


@permission_router.get("", status_code=status.HTTP_200_OK, name="admin.permission.read")
async def index(session: AsyncSession = Depends(get_db)):
    """Get all permissions grouped by module."""
    data = await PermissionService.get_permissions_grouped(session=session)
    if data is None:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Permissions fetched successfully")


@permission_router.get("/flat", status_code=status.HTTP_200_OK, name="admin.permission.list")
async def flat_list(session: AsyncSession = Depends(get_db)):
    """Get all permissions as a flat list."""
    data = await PermissionService.get_all(session=session)
    if data is None:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Permissions fetched successfully")


@permission_router.post("/sync", status_code=status.HTTP_200_OK, name="admin.permission.sync")
async def sync_permissions(session: AsyncSession = Depends(get_db)):
    """Sync permissions from all registered FastAPI routes."""
    from main import app as fastapi_app

    result = await PermissionService.sync_permissions(fastapi_app, session=session)
    return response(data=result, message="Permissions synced successfully")
