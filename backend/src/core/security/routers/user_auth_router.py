from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response

from ..schemas.user_login_schema import UserLoginResponseSchema, ForgotPasswordSchema, ResetPasswordSchema
from ..schemas.base_schema import LoginResponseSchema, APIResponseSchema
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository
from ...dependencies.service_dependency import get_service

from ..utils.hash import verify_password
from ..utils.auth import create_access_token
from ..utils import error_response, response
from ..utils.email import send_reset_password_email
from ...config.settings import settings
from itsdangerous import URLSafeTimedSerializer
from .. import InertiaDep
from fastapi import Request

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


@auth_router.get("/forgot-password", name="auth.forgot-password_page")
async def forgot_password_page(inertia: InertiaDep):
    return await inertia.render("ForgotPassword")


@auth_router.post("/forgot-password", name="auth.forgot-password")
async def forgot_password(
    request: Request,
    data: ForgotPasswordSchema,
    user_service: UserService = Depends(get_service(UserService, UserRepository)),
):
    user = await user_service.is_unique(email=data.email)
    if not user:
        # Prevent email enumeration by always returning success or a generic message
        return response(message="If your email is registered, you will receive a reset link.", data=None)

    serializer = URLSafeTimedSerializer(settings.APP_SECRET_KEY)
    token = serializer.dumps(data.email, salt="password-reset-salt")
    reset_link = f"{request.url.scheme}://{request.url.netloc}/login/reset-password?token={token}&email={data.email}"

    # Actually we need uow for sending email to fetch SMTP config
    await send_reset_password_email(data.email, reset_link, user_service.uow.session)
    return response(message="If your email is registered, you will receive a reset link.", data=None)


@auth_router.get("/reset-password", name="auth.reset-password_page")
async def reset_password_page(inertia: InertiaDep, token: str, email: str):
    return await inertia.render("ResetPassword", props={"token": token, "email": email})


@auth_router.post("/reset-password", name="auth.reset-password")
async def reset_password(
    data: ResetPasswordSchema,
    user_service: UserService = Depends(get_service(UserService, UserRepository)),
):
    if data.password != data.password_confirmation:
        return error_response(message="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST)

    serializer = URLSafeTimedSerializer(settings.APP_SECRET_KEY)
    try:
        email = serializer.loads(data.token, salt="password-reset-salt", max_age=3600)
    except Exception:
        return error_response(message="The reset link is invalid or has expired.", status_code=status.HTTP_400_BAD_REQUEST)

    if email != data.email:
        return error_response(message="Invalid request.", status_code=status.HTTP_400_BAD_REQUEST)

    # Need a method to get user by email
    # or just use uow
    user_model = await user_service.uow.repo.get_by_email(email)
    if not user_model:
        return error_response(message="Invalid request.", status_code=status.HTTP_400_BAD_REQUEST)

    from ..utils.hash import make_password
    user_model.password = make_password(data.password)
    await user_service.uow.repo.update(user_model)

    return response(message="Your password has been reset successfully. Please login.", data=None)
