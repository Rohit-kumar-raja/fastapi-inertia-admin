from ..models.route_model import RouteModel
from ..models.role_permission_link_model import RolePermissionLinkModel
from ..services.route_service import PermissionService
from ..services.privilege_service import PrivilegeService
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
            privileges_services = await PrivilegeService.get_all(session=session)
            record["privilege_ids"] = [privilege.id for privilege in privileges_services]
            await PermissionService.create(record, session=session)

    @staticmethod
    async def delete_all(session: AsyncSession):
        """
        Delete all routes from the database.
        """
        try:
            await session.execute(delete({RolePermissionLinkModel, RouteModel}))
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
