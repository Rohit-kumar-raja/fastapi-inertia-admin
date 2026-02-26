"""
SQLAlchemy user database adapter for fastapi-users.
Connects AppUserModel to fastapi-users' database layer.
"""
from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from apps.appuser.models.user_model import AppUserModel
from core.dependencies import get_db


async def get_user_db(
    session: AsyncSession = Depends(get_db),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, AppUserModel)
