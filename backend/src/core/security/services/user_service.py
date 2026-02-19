import time
from typing import Dict, List, Optional, Set
from sqlalchemy import delete, select, update
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import selectinload

from ..models.permission_model import PermissionModel
from ..models.role_model import RoleModel, RolePermissionLinkModel
from ..models.user_model import UserModel, UserRoleLinkModel
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.hash import make_password
from datatables import DataTables, DataTablesRequest


# In-memory permission cache: user_id -> (permissions_set, timestamp)
_permission_cache: Dict[str, tuple[Set[str], float]] = {}
_CACHE_TTL_SECONDS = 300  # 5 minutes


def _get_cached_permissions(user_id: str) -> Optional[Set[str]]:
    """Get cached permissions for a user, or None if expired/missing."""
    if user_id in _permission_cache:
        perms, ts = _permission_cache[user_id]
        if time.time() - ts < _CACHE_TTL_SECONDS:
            return perms
        del _permission_cache[user_id]
    return None


def _set_cached_permissions(user_id: str, perms: Set[str]):
    """Cache permissions for a user."""
    _permission_cache[user_id] = (perms, time.time())


def invalidate_permission_cache(user_id: Optional[str] = None):
    """Invalidate permission cache. If user_id is None, invalidate all."""
    if user_id is None:
        _permission_cache.clear()
    elif user_id in _permission_cache:
        del _permission_cache[user_id]


class UserService:
    """
    UserService handles the business logic and database operations for User.
    """

    @staticmethod
    async def create(data: dict, session: AsyncSession) -> Optional[UserModel]:
        """Create a new User."""
        try:
            role_ids = data.pop("role_ids", [])
            roles = await session.execute(select(RoleModel).where(RoleModel.id.in_(role_ids)))
            roles = roles.scalars().all()
            data["password"] = make_password(data["password"])
            instance = UserModel(**data)
            instance.roles = roles
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_all(session: AsyncSession) -> List[dict]:
        """Fetch all Users."""
        statement = select(UserModel).where(UserModel.deleted_at.is_(None)).options(selectinload(UserModel.roles))
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(uuid: UUID, session: AsyncSession) -> Optional[dict]:
        """Fetch a User by its UUID."""
        statement = (
            select(UserModel)
            .where(UserModel.id == uuid, UserModel.deleted_at.is_(None))
            .options(selectinload(UserModel.roles))
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def update(uuid: UUID, data: dict, session: AsyncSession) -> Optional[dict]:
        """Update an existing User."""
        try:
            async with session.begin():
                data.pop("id", None)
                role_ids = data.pop("role_ids", [])
                await session.execute(delete(UserRoleLinkModel).where(UserRoleLinkModel.auth_user_id == uuid))
                for role_id in role_ids:
                    session.add(UserRoleLinkModel(auth_user_id=uuid, auth_role_id=role_id))
                await session.execute(
                    update(UserModel).where(UserModel.id == uuid, UserModel.deleted_at.is_(None)).values(**data)
                )
            # Invalidate permission cache for this user
            invalidate_permission_cache(str(uuid))
            return await UserService.get_by_id(uuid, session)
        except Exception:
            await session.rollback()
            return None

    @staticmethod
    async def delete(uuid: UUID, session: AsyncSession) -> bool:
        """Soft delete a User by its UUID."""
        instance = await session.get(UserModel, uuid)
        if instance and instance.deleted_at is None:
            instance.deleted_at = datetime.utcnow()
            await session.commit()
            await session.refresh(instance)
            invalidate_permission_cache(str(uuid))
            return True
        return False

    @staticmethod
    async def is_unique(username: str = None, email: str = None, session: AsyncSession = None) -> bool:
        """Check if username or email already exists."""
        if username:
            statement = select(UserModel).where(UserModel.username == username, UserModel.deleted_at.is_(None))
            result = await session.execute(statement)
            if result.scalars().first() is not None:
                return True

        if email:
            statement = select(UserModel).where(UserModel.email == email, UserModel.deleted_at.is_(None))
            result = await session.execute(statement)
            if result.scalars().first() is not None:
                return True

        return False

    @staticmethod
    async def get_user_by_username(username: str, session: AsyncSession) -> Optional[UserModel]:
        statement = select(UserModel).where(UserModel.username == username, UserModel.deleted_at.is_(None))
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    def reset_password():
        pass

    @staticmethod
    async def get_user_permissions(user_id: UUID, session: AsyncSession) -> List[str]:
        """
        Fetch all permission names for a user through their roles.
        Uses in-memory caching for performance.
        """
        user_id_str = str(user_id)
        cached = _get_cached_permissions(user_id_str)
        if cached is not None:
            return list(cached)

        statement = (
            select(PermissionModel.name)
            .join(RolePermissionLinkModel, RolePermissionLinkModel.auth_permission_id == PermissionModel.id)
            .join(RoleModel, RoleModel.id == RolePermissionLinkModel.auth_role_id)
            .join(UserRoleLinkModel, UserRoleLinkModel.auth_role_id == RoleModel.id)
            .where(
                UserRoleLinkModel.auth_user_id == user_id,
                RoleModel.deleted_at.is_(None),
                PermissionModel.deleted_at.is_(None),
                PermissionModel.is_active.is_(True),
            )
            .distinct()
        )

        result = await session.execute(statement)
        permissions = set(result.scalars().all())
        _set_cached_permissions(user_id_str, permissions)
        return list(permissions)

    @staticmethod
    async def datatables(session: AsyncSession, request_data: DataTablesRequest) -> List[UserModel]:
        """Fetch all active and non-deleted Users."""
        statement = select(UserModel).filter_by(deleted_at=None, is_active=True).options(selectinload(UserModel.roles))
        datatables = DataTables(session, UserModel, statement)
        return await datatables.process(request_data=request_data)
