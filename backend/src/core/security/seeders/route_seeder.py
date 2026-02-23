from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete

from core.common.uow.uow import AsyncUnitOfWork
from core.security.models.permission_model import PermissionModel
from core.security.models.role_model import RolePermissionLinkModel
from core.security.repositories.permission_repository import PermissionRepository
from core.security.services.permission_service import PermissionService


class PermissionSeeder:
    """
    Seeder for PermissionModel.
    Auto-syncs permissions from FastAPI route names on startup.
    """

    @staticmethod
    async def run(session: AsyncSession):
        """
        Sync all permissions from the FastAPI app routes.
        """
        from main import app

        async with AsyncUnitOfWork(session, PermissionRepository) as perm_uow:
            perm_service = PermissionService(perm_uow)
            result = await perm_service.sync_permissions(app)
            
        print(f"✅ Permissions synced: {result}")

    @staticmethod
    async def delete_all(session: AsyncSession):
        """
        Delete all permissions from the database.
        """
        try:
            await session.execute(delete(RolePermissionLinkModel))
            await session.execute(delete(PermissionModel))
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
