from uuid import UUID
from fastapi import Request, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from ..schemas.route_schema import RouteSchema
from ..services.route_service import RouteService
from ..utils import error_response, response
from .. import get_db

routes_router = APIRouter(prefix="/administration/routes", tags=["routes"])


@routes_router.get("", status_code=status.HTTP_200_OK, name="admin.routes.read")
async def index(request: Request, session: AsyncSession = Depends(get_db)):
    """Get all the data"""
    data = await RouteService.get_all(session=session)
    if data is None:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")


@routes_router.get("/{uuid}", status_code=status.HTTP_200_OK, name="admin.routes.read")
async def edit(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Read or edit the data based on the given UUID."""
    data = await RouteService.get_by_id(uuid, session=session)
    if data is None:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")


@routes_router.post("", status_code=status.HTTP_201_CREATED, name="admin.routes.write")
async def create(permission: RouteSchema, session: AsyncSession = Depends(get_db)):
    """Create new data based on the request."""
    is_unique = await RouteService.is_unique(name=permission.name, parent_id=permission.parent_id, session=session)
    if is_unique:
        return error_response(message="Permission name already exists ", status_code=422)
    response_data = await RouteService.create(permission.model_dump(), session=session)
    return response(data=response_data, message="Data created successfully")


@routes_router.put("/{uuid}", status_code=status.HTTP_200_OK, name="admin.routes.edit")
async def update(role: RouteSchema, uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Update the data based on the given UUID."""
    data = await RouteService.update(uuid, role.model_dump(), session=session)
    return response(data=data, message="Data updated successfully")


@routes_router.delete("/{uuid}", status_code=status.HTTP_200_OK, name="admin.routes.delete")
async def destroy(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Delete the data based on the given UUID."""
    permision = await RouteService.get_by_id(uuid, session=session)
    if permision is None:
        return error_response(message="Data not found", status_code=404)
    if permision.children != []:
        return error_response(message="You can't delete the parent Route", status_code=400)

    data = await RouteService.delete(uuid, session=session)
    return response(data=data, message="Data deleted successfully")


@routes_router.get("/tree/sidebar", status_code=status.HTTP_200_OK, name="admin.routes.read")
async def get_route_tree(session: AsyncSession = Depends(get_db)):
    data = await RouteService.get_permission_tree(session=session)
    if data is None:
        return error_response(message="Permission Tree not found", status_code=404)
    return response(data=data, message="Permission Tree fetched successfully")
