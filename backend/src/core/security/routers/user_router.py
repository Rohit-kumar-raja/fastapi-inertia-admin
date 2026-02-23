from uuid import UUID
from fastapi import APIRouter, Depends, Request, status

from ..schemas.user_schema import UserBaseSchema, UserSchema, UserUpdateSchema
from ..services.user_service import UserService
from ..services.notification_service import NotificationService
from ..services.webpush_service import WebPushService

from ..repositories.user_repository import UserRepository
from ..repositories.notification_repository import NotificationRepository
from ..repositories.webpush_repository import WebPushRepository
from ...dependencies.service_dependency import get_service

from ..utils import response, error_response
from .. import InertiaDep
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
async def create(
    user: UserSchema,
    request: Request,
    user_service: UserService = Depends(get_service(UserService, UserRepository)),
    notif_service: NotificationService = Depends(get_service(NotificationService, NotificationRepository)),
    push_service: WebPushService = Depends(get_service(WebPushService, WebPushRepository))
):
    """Create new data based on the request."""
    if await user_service.is_unique(username=user.username):
        return error_response(message="Username already exists", status_code=422)

    if await user_service.is_unique(email=user.email):
        return error_response(message="Email already exists", status_code=422)

    response_data = await user_service.create(user.model_dump())

    current_user = request.state.user
    await notif_service.create_notification(
        user_id=current_user["id"],
        title="New User Created",
        message=f"User '{user.username}' has been created successfully.",
        type="success",
    )
    if settings.VAPID_PRIVATE_KEY:
        await push_service.send_to_user(
            user_id=current_user["id"],
            title="New User Created",
            message=f"User '{user.username}' has been created successfully.",
            notification_type="success",
        )

    return response(data=response_data, message="Data created successfully")


@user_router.get("/{uuid}", status_code=status.HTTP_200_OK, name="admin.user.detail")
async def edit(
    uuid: UUID,
    user_service: UserService = Depends(get_service(UserService, UserRepository))
):
    """Read or edit the data based on the given UUID."""
    data = await user_service.get_by_id(uuid)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")


@user_router.put(
    "/{uuid}",
    status_code=status.HTTP_200_OK,
    name="admin.user.edit",
    dependencies=[Depends(require_permission("admin.user.edit"))],
)
async def update(
    user: UserUpdateSchema,
    uuid: UUID,
    request: Request,
    user_service: UserService = Depends(get_service(UserService, UserRepository)),
    notif_service: NotificationService = Depends(get_service(NotificationService, NotificationRepository)),
    push_service: WebPushService = Depends(get_service(WebPushService, WebPushRepository))
):
    """Update the data based on the given UUID."""
    data = await user_service.update(uuid, user.model_dump())

    current_user = request.state.user
    await notif_service.create_notification(
        user_id=current_user["id"],
        title="User Updated",
        message=f"User '{user.username}' has been updated.",
        type="info",
    )
    if settings.VAPID_PRIVATE_KEY:
        await push_service.send_to_user(
            user_id=current_user["id"],
            title="User Updated",
            message=f"User '{user.username}' has been updated.",
            notification_type="info",
        )

    return response(data=data, message="Data updated successfully")


@user_router.delete(
    "/{uuid}",
    status_code=status.HTTP_200_OK,
    name="admin.user.delete",
    dependencies=[Depends(require_permission("admin.user.delete"))],
)
async def destroy(
    uuid: UUID,
    request: Request,
    user_service: UserService = Depends(get_service(UserService, UserRepository)),
    notif_service: NotificationService = Depends(get_service(NotificationService, NotificationRepository)),
    push_service: WebPushService = Depends(get_service(WebPushService, WebPushRepository))
):
    """Delete the data based on the given UUID."""
    data = await user_service.delete(uuid)
    if not data:
        return error_response(message="Data not found", status_code=404)

    current_user = request.state.user
    await notif_service.create_notification(
        user_id=current_user["id"],
        title="User Deleted",
        message="A user has been deleted.",
        type="warning",
    )
    if settings.VAPID_PRIVATE_KEY:
        await push_service.send_to_user(
            user_id=current_user["id"],
            title="User Deleted",
            message="A user has been deleted.",
            notification_type="warning",
        )

    return response(data=data, message="Data deleted successfully")


@user_router.post(
    "/reset-password/{uuid}",
    status_code=status.HTTP_200_OK,
    name="admin.user.reset-password",
    dependencies=[Depends(require_permission("admin.user.edit"))],
)
async def reset_password(
    uuid: UUID,
    user_service: UserService = Depends(get_service(UserService, UserRepository))
):
    """Reset the password based on the given UUID."""
    data = await user_service.reset_password(uuid)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Password reset successfully")


@user_router.post("/filter", status_code=status.HTTP_200_OK, name="admin.user.datatables")
async def filter(
    request_data: DataTablesRequest,
    user_service: UserService = Depends(get_service(UserService, UserRepository))
):
    """Get all"""
    data = await user_service.datatables(request_data)
    if not data:
        return error_response(message="Data not found", status_code=404)
    return response(data=data, message="Data fetched successfully")
