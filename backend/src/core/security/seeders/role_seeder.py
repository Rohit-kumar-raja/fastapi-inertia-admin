from ..services.permission_service import PermissionService
from ..services.role_service import RoleService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete
from core.security.models.role_model import RoleModel


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

        # Insert the data into the database using a loop
        for record in records:
            permissions = await PermissionService.get_all(session=session)
            if not permissions:
                raise ValueError("No permissions found in the database. Run PermissionSeeder first.")
            record["permission_ids"] = [perm.id for perm in permissions]
            await RoleService.create(record, session=session)

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
