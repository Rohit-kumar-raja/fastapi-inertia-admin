from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete

from core.common.uow.uow import AsyncUnitOfWork
from core.security.models.role_model import RoleModel
from core.security.repositories.role_repository import RoleRepository
from core.security.repositories.permission_repository import PermissionRepository
from core.security.services.role_service import RoleService
from core.security.services.permission_service import PermissionService


class RoleSeeder:
    """
    Seeder for RoleModel to populate initial data.
    """

    @staticmethod
    async def run(session: AsyncSession):
        """
        Run the seeder to insert sample data into the database.
        """
        records = [
            {
                "name": "Admin",
            },
            {
                "name": "Editor",
            },
        ]

        async with AsyncUnitOfWork(session, PermissionRepository) as perm_uow:
            perm_service = PermissionService(perm_uow)
            permissions = await perm_service.get_all()

        if not permissions:
            raise ValueError("No permissions found in the database. Run PermissionSeeder first.")

        async with AsyncUnitOfWork(session, RoleRepository) as role_uow:
            role_service = RoleService(role_uow)
            for record in records:
                record["permission_ids"] = [str(perm.id) for perm in permissions]
                await role_service.create(record)

    @staticmethod
    async def delete_all(session: AsyncSession):
        """
        Delete all roles from the database.
        """
        try:
            await session.execute(delete(RoleModel))
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
