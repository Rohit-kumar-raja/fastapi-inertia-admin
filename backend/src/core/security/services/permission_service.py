from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.permission_model import PermissionModel


class PermissionService:
    """
    PermissionService handles business logic for action-based permissions.
    Supports auto-syncing permissions from FastAPI route names.
    """

    @staticmethod
    async def create(data: dict, session: AsyncSession) -> PermissionModel:
        """Create a new Permission."""
        try:
            instance = PermissionModel(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_all(session: AsyncSession) -> List[PermissionModel]:
        """Fetch all active and non-deleted Permissions."""
        statement = select(PermissionModel).where(PermissionModel.deleted_at.is_(None))
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(uuid: UUID, session: AsyncSession) -> Optional[PermissionModel]:
        """Fetch a Permission by its UUID."""
        statement = select(PermissionModel).where(
            PermissionModel.id == uuid,
            PermissionModel.deleted_at.is_(None),
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def get_by_name(name: str, session: AsyncSession) -> Optional[PermissionModel]:
        """Fetch a Permission by its name."""
        statement = select(PermissionModel).where(
            PermissionModel.name == name,
            PermissionModel.deleted_at.is_(None),
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def update(uuid: UUID, data: dict, session: AsyncSession) -> Optional[PermissionModel]:
        """Update an existing Permission."""
        try:
            data.pop("id", None)
            await session.execute(
                update(PermissionModel)
                .where(
                    PermissionModel.id == uuid,
                    PermissionModel.deleted_at.is_(None),
                )
                .values(**data)
            )
            await session.commit()
            return await PermissionService.get_by_id(uuid, session)
        except Exception:
            await session.rollback()
            return None

    @staticmethod
    async def delete(uuid: UUID, session: AsyncSession) -> bool:
        """Soft delete a Permission by its UUID."""
        instance = await session.get(PermissionModel, uuid)
        if instance and instance.deleted_at is None:
            instance.deleted_at = datetime.utcnow()
            await session.commit()
            return True
        return False

    @staticmethod
    async def get_permissions_grouped(session: AsyncSession) -> List[Dict]:
        """Fetch all permissions grouped by module."""
        permissions = await PermissionService.get_all(session)
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

    @staticmethod
    async def sync_permissions(app, session: AsyncSession) -> dict:
        """
        Scan all FastAPI routes and upsert permissions into the database.
        Returns a summary of created, existing, and deactivated permissions.
        """
        from fastapi.routing import APIRoute

        route_names = set()
        for route in app.routes:
            if isinstance(route, APIRoute) and route.name:
                route_names.add(route.name)

        # Get existing permissions
        existing = await PermissionService.get_all(session)
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
                session.add(perm)
                created += 1

        await session.commit()

        return {
            "created": created,
            "reactivated": reactivated,
            "existing": len(existing_map),
            "total_routes": len(route_names),
        }
