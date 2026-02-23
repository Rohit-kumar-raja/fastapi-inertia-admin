from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response

from ..schemas.user_login_schema import UserLoginResponseSchema
from ..schemas.base_schema import LoginResponseSchema
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository
from ...dependencies.service_dependency import get_service

from ..utils.hash import verify_password
from ..utils.auth import create_access_token
from ..utils import error_response, response
from .. import InertiaDep

auth_router = APIRouter(prefix="/login", tags=["auth"])


@auth_router.get("", name="user.login")
async def login_page(inertia: InertiaDep):
    return await inertia.render("Login")


@auth_router.post(
    "",
    response_model=LoginResponseSchema[UserLoginResponseSchema],
    name="user.login.post",
    status_code=status.HTTP_200_OK,
)
async def login(
    responses: Response,
    login: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_service(UserService, UserRepository)),
):
    user_data = await user_service.get_user_by_username(login.username)
    if not user_data:
        return error_response(message="User not found", status_code=status.HTTP_404_NOT_FOUND)
    if not user_data.is_active:
        return error_response(message="User is inactive", status_code=status.HTTP_400_BAD_REQUEST)
    if not verify_password(login.password, user_data.password):
        return error_response(message="Invalid password", status_code=status.HTTP_400_BAD_REQUEST)

    token = create_access_token(user_data)

    permissions = []
    if user_data.is_superuser:
        permissions = ["*"]
    else:
        permissions = await user_service.get_user_permissions(user_data.id)

    data = {"user": user_data.__dict__}
    data["access_token"] = token
    data["permissions"] = permissions

    response_data = response(data=data, message="User has logged in successfully.")
    response_data["access_token"] = token
    responses.set_cookie(
        "access_token", token, httponly=True, secure=False, samesite="lax", path="/", max_age=60 * 60 * 24 * 7
    )
    return response_data


@auth_router.post("/reset-password", name="auth.reset-password")
async def reset_password():
    pass


@auth_router.post("/forgot-password", name="auth.forgot-password")
async def forgot_password():
    pass
