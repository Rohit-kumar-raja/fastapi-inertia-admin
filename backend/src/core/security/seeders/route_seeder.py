from ..models.permission_model import PermissionModel
from ..models.role_model import RolePermissionLinkModel
from ..services.permission_service import PermissionService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete


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

        result = await PermissionService.sync_permissions(app, session=session)
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
