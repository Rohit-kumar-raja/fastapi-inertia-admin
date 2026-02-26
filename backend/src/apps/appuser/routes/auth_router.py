"""
Auth router for the mobile application (appuser).
Sets up fastapi-users with full auth capabilities:
- JWT login
- Registration
- Password reset
- Email verification
"""
import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users import models

from apps.appuser.models.user_model import AppUserModel
from apps.appuser.schemas.user_schema import UserRead, UserCreate, UserUpdate
from apps.appuser.services.user_manager import get_user_manager
from core.config.settings import settings


# ─── Auth Backend ─────────────────────────────────────────────────────────────
bearer_transport = BearerTransport(tokenUrl="api/auth/login")


def get_jwt_strategy() -> JWTStrategy[models.UP, models.ID]:
    return JWTStrategy(secret=settings.APP_SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users_instance = FastAPIUsers[AppUserModel, uuid.UUID](
    get_user_manager, [auth_backend]
)


# ─── Build the Router ────────────────────────────────────────────────────────
appuser_router = APIRouter(tags=["appuser"])

# Auth routes (login / logout)
appuser_router.include_router(
    fastapi_users_instance.get_auth_router(auth_backend),
    prefix="/auth",
)

# Registration
appuser_router.include_router(
    fastapi_users_instance.get_register_router(UserRead, UserCreate),
    prefix="/auth",
)

# Password reset (forgot-password / reset-password)
appuser_router.include_router(
    fastapi_users_instance.get_reset_password_router(),
    prefix="/auth",
)

# Email verification
appuser_router.include_router(
    fastapi_users_instance.get_verify_router(UserRead),
    prefix="/auth",
)

# User profile management
appuser_router.include_router(
    fastapi_users_instance.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)
