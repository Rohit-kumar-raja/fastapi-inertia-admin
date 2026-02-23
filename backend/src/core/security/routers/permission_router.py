from fastapi import APIRouter, Depends, status

from ..services.permission_service import PermissionService
from ..repositories.permission_repository import PermissionRepository
from ...dependencies.service_dependency import get_service

from ..utils import response, error_response
from .. import InertiaDep


permission_router = APIRouter(prefix="/administration/permissions", tags=["permissions"])


@permission_router.get("", status_code=status.HTTP_200_OK, name="admin.permission.read")
async def index(
    perm_service: PermissionService = Depends(get_service(PermissionService, PermissionRepository))
):
    """Get all permissions grouped by module."""
    data = await perm_service.get_permissions_grouped()
    if data is None:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Permissions fetched successfully")


@permission_router.get("/flat", status_code=status.HTTP_200_OK, name="admin.permission.list")
async def flat_list(
    perm_service: PermissionService = Depends(get_service(PermissionService, PermissionRepository))
):
    """Get all permissions as a flat list."""
    data = await perm_service.get_all()
    if data is None:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Permissions fetched successfully")


@permission_router.post("/sync", status_code=status.HTTP_200_OK, name="admin.permission.sync")
async def sync_permissions(
    perm_service: PermissionService = Depends(get_service(PermissionService, PermissionRepository))
):
    """Sync permissions from all registered FastAPI routes."""
    from main import app as fastapi_app

    result = await perm_service.sync_permissions(fastapi_app)
    return response(data=result, message="Permissions synced successfully")
