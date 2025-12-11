import contextvars
import jwt
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from ..models.user_model import UserModel
from datetime import datetime, timedelta, timezone
from ...config.settings import settings


SECRET_KEY = settings.APP_SECRET_KEY
ALGORITHM = settings.APP_ALGORITHM
EXCEPT_URL = ["/token", "/docs", "/openapi.json", "/auth/user/login"]
ACCESS_TOKEN_EXPIRE_MINUTES = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Define a global context variable for request
_request_ctx_var = contextvars.ContextVar("request")


def request() -> Request:
    return _request_ctx_var.get()


def set_request_context(request: Request):
    """Stores the request globally in context."""
    return _request_ctx_var.set(request)


def reset_request_context(token):
    """Resets the request context variable."""
    _request_ctx_var.reset(token)


def create_access_token(user: UserModel, additional_info: dict = {}) -> str:
    if not user:
        return None
    to_encode = {"id": str(user.id), "sub": user.username}
    if ACCESS_TOKEN_EXPIRE_MINUTES is not None:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
    to_encode.update(additional_info)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_user(user: SQLModel = UserModel) -> SQLModel:
#     request_data = request()
#     if not hasattr(request_data, "state"):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No request state found")
#     async with AsyncSession(async_engine) as session:
#         user = await session.get(user, request_data.state.user["id"] or None)
#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#         return user


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return username from token
    except InvalidTokenError:
        return None
