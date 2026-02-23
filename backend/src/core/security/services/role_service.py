from typing import List, Optional
from uuid import UUID

from datetime import datetime
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, select, update

from ..models.permission_model import PermissionModel
from ..models.role_model import RoleModel, RolePermissionLinkModel
from datatables import DataTables, DataTablesRequest, DataTablesResponse

from  ...common.uow.uow import AsyncUnitOfWork
from ..repositories.role_repository import RoleRepository
from ..repositories.permission_repository import PermissionRepository

class RoleService:
    """
    RoleService handles the business logic and database operations for Role
    using injected UoW.
    """
    def __init__(self, uow: AsyncUnitOfWork[RoleRepository]):
        self.uow = uow

    async def create(self, data: dict) -> Optional[RoleModel]:
        """Create a new Role."""
        permission_ids = data.pop("permission_ids", [])
        permission_repo = self.uow.get_repo(PermissionRepository)
        permissions = await permission_repo.get_permissions_by_ids(permission_ids)
        
        instance = RoleModel(**data)
        instance.permissions = permissions
        await self.uow.repo.add(instance)
        return instance

    async def get_all(self) -> List[RoleModel]:
        """Fetch all Roles."""
        return await self.uow.repo.get_all_with_permissions()

    async def get_by_id(self, uuid: UUID) -> Optional[RoleModel]:
        """Fetch a Role by its UUID."""
        return await self.uow.repo.get_by_id_with_permissions(str(uuid))

    async def update(self, uuid: UUID, data: dict) -> Optional[RoleModel]:
        """Update an existing Role."""
        data.pop("id", None)
        if "permission_ids" in data:
            permission_ids = data.pop("permission_ids")
            await self.uow.session.execute(
                delete(RolePermissionLinkModel).where(RolePermissionLinkModel.auth_role_id == uuid)
            )
            for permission_id in permission_ids:
                self.uow.session.add(RolePermissionLinkModel(auth_permission_id=permission_id, auth_role_id=uuid))
        
        await self.uow.session.execute(
            update(RoleModel).where(RoleModel.id == uuid, RoleModel.deleted_at.is_(None)).values(**data)
        )
        return await self.get_by_id(uuid)

    async def delete(self, uuid: UUID) -> bool:
        """Soft delete a Role if it is active and not already deleted."""
        instance = await self.uow.repo.get_by_id(uuid)
        if instance and instance.deleted_at is None:
            instance.deleted_at = datetime.utcnow()
            await self.uow.repo.update(instance)
            return True
        return False

    async def is_unique(self, name: str) -> bool:
        role = await self.uow.repo.get_by_name(name)
        return role is not None

    async def datatables(self, request_data: DataTablesRequest) -> List[RoleModel]:
        """Fetch all active and non-deleted Roles."""
        statement = (
            select(RoleModel)
            .filter_by(deleted_at=None, is_active=True)
            .options(selectinload(RoleModel.permissions))
        )
        datatables = DataTables(self.uow.session, RoleModel, statement)
        return await datatables.process(request_data=request_data)
