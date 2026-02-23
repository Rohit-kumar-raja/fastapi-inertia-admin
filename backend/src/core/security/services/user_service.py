from typing import List, Optional
from sqlalchemy import delete, select, update
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import selectinload

from ..models.permission_model import PermissionModel
from ..models.role_model import RoleModel, RolePermissionLinkModel
from ..models.user_model import UserModel, UserRoleLinkModel
from ..utils.hash import make_password
from datatables import DataTables, DataTablesRequest
from core.common.uow.uow import AsyncUnitOfWork
from ..repositories.user_repository import UserRepository
from ..repositories.role_repository import RoleRepository


class UserService:
    """
    UserService handles the business logic and database operations for User
    with UoW and Repositories injected.
    """

    def __init__(self, uow: AsyncUnitOfWork[UserRepository]):
        self.uow = uow

    async def create(self, data: dict) -> Optional[UserModel]:
        """Create a new User."""
        try:
            role_ids = data.pop("role_ids", [])
            role_repo = self.uow.get_repo(RoleRepository)
            roles = await role_repo.get_roles_by_ids(role_ids)
            data["password"] = make_password(data["password"])
            instance = UserModel(**data)
            instance.roles = roles
            await self.uow.repo.add(instance)
            return instance
        except Exception as e:
            raise e

    async def get_all(self) -> List[UserModel]:
        """Fetch all Users."""
        return await self.uow.repo.get_all_active_users()

    async def get_by_id(self, uuid: UUID) -> Optional[UserModel]:
        """Fetch a User by its UUID."""
        return await self.uow.repo.get_by_id_with_roles(str(uuid))

    async def update(self, uuid: UUID, data: dict) -> Optional[UserModel]:
        """Update an existing User."""
        data.pop("id", None)
        role_ids = data.pop("role_ids", [])

        # We perform the relationship link deletes manually here or we could put this in the repo
        await self.uow.session.execute(
            delete(UserRoleLinkModel).where(UserRoleLinkModel.security_user_id == uuid)
        )
        for role_id in role_ids:
            self.uow.session.add(
                UserRoleLinkModel(security_user_id=uuid, security_role_id=role_id)
            )

        await self.uow.session.execute(
            update(UserModel)
            .where(UserModel.id == uuid)
            .values(**data)
        )
        return await self.get_by_id(uuid)

    async def delete(self, uuid: UUID) -> bool:
        """Soft delete a User by its UUID."""
        instance = await self.uow.repo.get_by_id(uuid)
        if instance:
            await self.uow.repo.delete(instance)
            return True
        return False

    async def is_unique(self, username: str = None, email: str = None) -> bool:
        """Check if username or email already exists."""
        if username:
            user = await self.uow.repo.get_by_username(username)
            if user:
                return True
        if email:
            user = await self.uow.repo.get_by_email(email)
            if user:
                return True
        return False

    async def get_user_by_username(self, username: str) -> Optional[UserModel]:
        return await self.uow.repo.get_by_username(username)

    async def reset_password(self, uuid: UUID) -> Optional[dict]:
        default_password = make_password("password123")
        await self.uow.session.execute(
            update(UserModel)
            .where(UserModel.id == uuid)
            .values(password=default_password)
        )
        return await self.get_by_id(uuid)

    async def get_user_permissions(self, user_id: UUID) -> List[str]:
        """
        Fetch all permission names for a user through their roles.
        """
        statement = (
            select(PermissionModel.name)
            .join(
                RolePermissionLinkModel,
                RolePermissionLinkModel.security_permission_id == PermissionModel.id,
            )
            .join(RoleModel, RoleModel.id == RolePermissionLinkModel.security_role_id)
            .join(UserRoleLinkModel, UserRoleLinkModel.security_role_id == RoleModel.id)
            .where(
                UserRoleLinkModel.security_user_id == user_id,
                PermissionModel.is_active.is_(True),
            )
            .distinct()
        )

        result = await self.uow.session.execute(statement)
        permissions = set(result.scalars().all())
        return list(permissions)

    async def datatables(self, request_data: DataTablesRequest) -> List[UserModel]:
        """Fetch all active and non-deleted Users."""
        statement = (
            select(UserModel)
            .filter_by(is_active=True)
            .options(selectinload(UserModel.roles))
        )
        datatables = DataTables(self.uow.session, UserModel, statement)
        return await datatables.process(request_data=request_data)
