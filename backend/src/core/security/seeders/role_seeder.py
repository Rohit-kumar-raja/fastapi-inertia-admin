from ..services.route_service import RouteService
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
            routes_services = await RouteService.get_all(session=session)
            if not routes_services:
                raise ValueError("No routes found in the database.")
            record["route_ids"] = [route.id for route in routes_services]
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
