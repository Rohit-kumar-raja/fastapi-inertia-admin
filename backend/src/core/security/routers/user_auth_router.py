from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status,Response
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user_login_schema import UserLoginResponseSchema
from ..schemas.base_schema import LoginResponseSchema
from ..services.user_service import UserService
from ..utils.hash import verify_password
from ..utils.auth import create_access_token
from ..utils import error_response, response
from .. import get_db

auth_router = APIRouter(prefix="/login", tags=["auth"])


@auth_router.post(
    "",
    response_model=LoginResponseSchema[UserLoginResponseSchema],
    name="admin.user.login",
    status_code=status.HTTP_200_OK,
)
async def login(
    responses: Response,
    login: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    user_data = await UserService.get_user_by_username(login.username, session=session)
    if not user_data:
        return error_response(message="User not found", status_code=status.HTTP_404_NOT_FOUND)
    if not user_data.is_active:
        return error_response(message="User is inactive", status_code=status.HTTP_400_BAD_REQUEST)
    if not verify_password(login.password, user_data.password):
        return error_response(message="Invalid password", status_code=status.HTTP_400_BAD_REQUEST)
    token = create_access_token(user_data)
    data = {"user": user_data.__dict__}
    data["access_token"] = token
    response_data = response(data=data, message="User has logged in successfully.")
    response_data["access_token"] = token
    responses.set_cookie("access_token", token, httponly=True, secure=False, samesite="lax",path="/",max_age=60*60*24*7)    
    return response_data


async def reset_password(self):
    pass


async def forgot_password(self):
    pass
