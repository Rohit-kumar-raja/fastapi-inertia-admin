from ..models.route_model import RouteModel,RolePermissionLinkModel
from ..services.route_service import RouteService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete


class RouteSeeder:
    """
    Seeder for RouteModel to populate initial data.
    """

    @staticmethod
    async def run(session: AsyncSession):
        """
        Run the seeder to insert sample data into the database.
        """
        records = [
            {
                "name": "Scada",
            },
            {
                "name": "Admin",
            },
            {
                "name": "Vision",
            },
        ]

        # Insert the data into the database using a loop
        for record in records:
            await RouteService.create(record, session=session)

    @staticmethod
    async def delete_all(session: AsyncSession):
        """
        Delete all routes from the database.
        """
        try:
            await session.execute(delete(RolePermissionLinkModel))
            await session.execute(delete(RouteModel))
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
