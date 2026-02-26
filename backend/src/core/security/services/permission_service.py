from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from ..models.permission_model import PermissionModel
from  ...common.uow.uow import AsyncUnitOfWork
from ..repositories.permission_repository import PermissionRepository


class PermissionService:
    """
    PermissionService handles business logic for action-based permissions.
    Supports auto-syncing permissions from FastAPI route names.
    """
    def __init__(self, uow: AsyncUnitOfWork[PermissionRepository]):
        self.uow = uow

    async def create(self, data: dict) -> PermissionModel:
        """Create a new Permission."""
        instance = PermissionModel(**data)
        await self.uow.repo.add(instance)
        return instance

    async def get_all(self) -> List[PermissionModel]:
        """Fetch all active and non-deleted Permissions."""
        return await self.uow.repo.get_all_active()

    async def get_by_id(self, uuid: UUID) -> Optional[PermissionModel]:
        """Fetch a Permission by its UUID."""
        return await self.uow.repo.get_by_id(str(uuid))

    async def get_by_name(self, name: str) -> Optional[PermissionModel]:
        """Fetch a Permission by its name."""
        statement = select(PermissionModel).where(
            PermissionModel.name == name
        )
        result = await self.uow.session.execute(statement)
        return result.scalars().first()

    async def update(self, uuid: UUID, data: dict) -> Optional[PermissionModel]:
        """Update an existing Permission."""
        data.pop("id", None)
        await self.uow.session.execute(
            update(PermissionModel)
            .where(
                PermissionModel.id == uuid
            )
            .values(**data)
        )
        return await self.get_by_id(uuid)

    async def delete(self, uuid: UUID) -> bool:
        """Soft delete a Permission by its UUID."""
        instance = await self.uow.repo.get_by_id(str(uuid))
        if instance:
            await self.uow.repo.delete(instance)
            return True
        return False

    async def get_permissions_grouped(self) -> List[Dict]:
        """Fetch all permissions grouped by module."""
        permissions = await self.get_all()
        groups: Dict[str, List[dict]] = {}
        for perm in permissions:
            module = perm.module
            if module not in groups:
                groups[module] = []
            groups[module].append({
                "id": str(perm.id),
                "name": perm.name,
                "module": perm.module,
                "description": perm.description,
                "is_active": perm.is_active,
            })
        return [{"module": module, "permissions": perms} for module, perms in groups.items()]

    @staticmethod
    def _extract_module(route_name: str) -> str:
        """Extract module from route name. E.g. 'admin.role.read' -> 'role'."""
        parts = route_name.split(".")
        if len(parts) >= 2:
            return parts[-2]
        return parts[0]

    @staticmethod
    def _generate_description(route_name: str) -> str:
        """Generate a human-readable description from route name."""
        parts = route_name.split(".")
        if len(parts) >= 2:
            action = parts[-1].replace("-", " ").title()
            module = parts[-2].replace("-", " ").title()
            return f"{action} {module}"
        return route_name.replace(".", " ").replace("-", " ").title()

    async def sync_permissions(self, app) -> dict:
        """
        Scan all FastAPI routes and upsert permissions into the database.
        Returns a summary of created, existing, and deactivated permissions.
        """
        from fastapi.routing import APIRoute
        from ...middlewares.rbac_middleware import SKIP_PREFIXES, SKIP_ROUTE_NAMES

        route_names = set()
        for route in app.routes:
            if isinstance(route, APIRoute) and route.name:
                if route.name in SKIP_ROUTE_NAMES:
                    continue
                if any(route.path.startswith(prefix) for prefix in SKIP_PREFIXES):
                    continue
                route_names.add(route.name)

        # Get existing permissions
        existing = await self.get_all()
        existing_map = {p.name: p for p in existing}

        created = 0
        reactivated = 0

        for name in route_names:
            if name in existing_map:
                # Re-activate if soft-deleted
                perm = existing_map[name]
                if not perm.is_active:
                    perm.is_active = True
                    reactivated += 1
            else:
                # Create new permission
                perm = PermissionModel(
                    name=name,
                    module=PermissionService._extract_module(name),
                    description=PermissionService._generate_description(name),
                    is_active=True,
                )
                self.uow.session.add(perm)
                created += 1

        return {
            "created": created,
            "reactivated": reactivated,
            "existing": len(existing_map),
            "total_routes": len(route_names),
        }
