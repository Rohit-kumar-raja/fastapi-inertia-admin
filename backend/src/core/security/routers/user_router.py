from uuid import UUID
from fastapi import APIRouter, Depends, status,Body
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user_schema import UserBaseSchema, UserSchema
from ..services.user_service import UserService
from ..utils import response, error_response
from .. import get_db,InertiaDep
from datatables import DataTablesRequest


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("", status_code=status.HTTP_200_OK, name="admin.user.read")
async def index(inertia:InertiaDep):
    return inertia.render("Admin/Users/Index")


@user_router.post("", status_code=status.HTTP_201_CREATED, name="admin.user.write")
async def create(user: UserSchema, session: AsyncSession = Depends(get_db)):
    """Create new data based on the request."""
    # Check username uniqueness
    if await UserService.is_unique(username=user.username, session=session):
        return error_response(message="Username already exists", status_code=422)
    
    # Check email uniqueness
    if await UserService.is_unique(email=user.email, session=session):
        return error_response(message="Email already exists", status_code=422)
    
    response_data = await UserService.create(user.model_dump(), session=session)
    return response(data=response_data, message="Data created successfully")


@user_router.get("/{uuid}", status_code=status.HTTP_200_OK, name="admin.user.read")
async def edit(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Read or edit the data based on the given UUID."""
    data = await UserService.get_by_id(uuid, session=session)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")


@user_router.put("/{uuid}", status_code=status.HTTP_200_OK, name="admin.user.edit")
async def update(user: UserBaseSchema, uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Update the data based on the given UUID."""
    data = await UserService.update(uuid, user.model_dump(), session)
    return response(data=data, message="Data updated successfully")


@user_router.delete("/{uuid}", status_code=status.HTTP_200_OK, name="admin.user.delete")
async def destroy(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Delete the data based on the given UUID."""
    data = await UserService.delete(uuid, session=session)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data deleted successfully")


@user_router.post("/reset-password/{uuid}", status_code=status.HTTP_200_OK, name="admin.user.reset-password")
async def reset_password(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Reset the password based on the given UUID."""
    data = await UserService.reset_password(uuid, session)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Password reset successfully")


@user_router.post("/filter", status_code=status.HTTP_200_OK, name="admin.user.datatables")
async def filter(request_data: DataTablesRequest, session: AsyncSession = Depends(get_db)):
    """Get all"""
    data = await UserService().datatables(session, request_data)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")
