from uuid import UUID
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user_schema import UserBaseSchema, UserSchema
from ..services.user_service import UserService
from ..services.notification_service import NotificationService
from ..services.webpush_service import WebPushService
from ..utils import response, error_response
from .. import get_db, InertiaDep
from ...dependencies.permission_dependency import require_permission
from ...config.settings import settings
from datatables import DataTablesRequest


user_router = APIRouter(prefix="/administration/users", tags=["users"])


@user_router.get("", status_code=status.HTTP_200_OK, name="admin.user.read")
async def index(inertia: InertiaDep):
    return await inertia.render("Admin/Users/Index")


@user_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    name="admin.user.write",
    dependencies=[Depends(require_permission("admin.user.write"))],
)
async def create(user: UserSchema, request: Request, session: AsyncSession = Depends(get_db)):
    """Create new data based on the request."""
    # Check username uniqueness
    if await UserService.is_unique(username=user.username, session=session):
        return error_response(message="Username already exists", status_code=422)

    # Check email uniqueness
    if await UserService.is_unique(email=user.email, session=session):
        return error_response(message="Email already exists", status_code=422)

    response_data = await UserService.create(user.model_dump(), session=session)

    # Send notification to the admin who created the user
    current_user = request.state.user
    await NotificationService.create_notification(
        user_id=current_user["id"],
        title="New User Created",
        message=f"User '{user.username}' has been created successfully.",
        type="success",
        session=session,
    )
    if settings.VAPID_PRIVATE_KEY:
        await WebPushService.send_to_user(
            user_id=current_user["id"],
            title="New User Created",
            message=f"User '{user.username}' has been created successfully.",
            notification_type="success",
            session=session,
        )

    return response(data=response_data, message="Data created successfully")


@user_router.get("/{uuid}", status_code=status.HTTP_200_OK, name="admin.user.detail")
async def edit(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Read or edit the data based on the given UUID."""
    data = await UserService.get_by_id(uuid, session=session)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")


@user_router.put(
    "/{uuid}",
    status_code=status.HTTP_200_OK,
    name="admin.user.edit",
    dependencies=[Depends(require_permission("admin.user.edit"))],
)
async def update(user: UserBaseSchema, uuid: UUID, request: Request, session: AsyncSession = Depends(get_db)):
    """Update the data based on the given UUID."""
    data = await UserService.update(uuid, user.model_dump(), session)

    # Send notification
    current_user = request.state.user
    await NotificationService.create_notification(
        user_id=current_user["id"],
        title="User Updated",
        message=f"User '{user.username}' has been updated.",
        type="info",
        session=session,
    )
    if settings.VAPID_PRIVATE_KEY:
        await WebPushService.send_to_user(
            user_id=current_user["id"],
            title="User Updated",
            message=f"User '{user.username}' has been updated.",
            notification_type="info",
            session=session,
        )

    return response(data=data, message="Data updated successfully")


@user_router.delete(
    "/{uuid}",
    status_code=status.HTTP_200_OK,
    name="admin.user.delete",
    dependencies=[Depends(require_permission("admin.user.delete"))],
)
async def destroy(uuid: UUID, request: Request, session: AsyncSession = Depends(get_db)):
    """Delete the data based on the given UUID."""
    data = await UserService.delete(uuid, session=session)
    if not data:
        return error_response(message="Data not found", status_code=404)

    # Send notification
    current_user = request.state.user
    await NotificationService.create_notification(
        user_id=current_user["id"],
        title="User Deleted",
        message="A user has been deleted.",
        type="warning",
        session=session,
    )
    if settings.VAPID_PRIVATE_KEY:
        await WebPushService.send_to_user(
            user_id=current_user["id"],
            title="User Deleted",
            message="A user has been deleted.",
            notification_type="warning",
            session=session,
        )

    return response(data=data, message="Data deleted successfully")


@user_router.post(
    "/reset-password/{uuid}",
    status_code=status.HTTP_200_OK,
    name="admin.user.reset-password",
    dependencies=[Depends(require_permission("admin.user.edit"))],
)
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
