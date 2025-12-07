from ..services.route_service import PermissionService
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
                "name": "Role1",
            },
            {
                "name": "Role2",
            },
        ]

        # Insert the data into the database using a loop
        for record in records:
            permission_services = await PermissionService.get_all(session=session)
            if not permission_services:
                raise ValueError("No routes found in the database.")
            record["permission_ids"] = [permission.id for permission in permission_services]
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
