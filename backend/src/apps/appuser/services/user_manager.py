"""
UserManager for the mobile app.
Handles token secrets and hooks like on_after_forgot_password.
"""
import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase

from apps.appuser.models.user_model import AppUserModel
from apps.appuser.repositories.user_db import get_user_db
from core.config.settings import settings


class UserManager(UUIDIDMixin, BaseUserManager[AppUserModel, uuid.UUID]):
    reset_password_token_secret = settings.APP_SECRET_KEY
    verification_token_secret = settings.APP_SECRET_KEY

    async def on_after_register(
        self, user: AppUserModel, request: Request | None = None
    ):
        print(f"[AppUser] User {user.id} ({user.email}) has registered.")

    async def on_after_forgot_password(
        self, user: AppUserModel, token: str, request: Request | None = None
    ):
        """
        Called by fastapi-users after generating the reset token.
        TODO: Integrate email sending for mobile app users.
        For now, log the token for development purposes.
        """
        print(f"[AppUser] User {user.id} forgot password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: AppUserModel, token: str, request: Request | None = None
    ):
        print(f"[AppUser] Verification requested for {user.id}. Token: {token}")


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
):
    yield UserManager(user_db)
