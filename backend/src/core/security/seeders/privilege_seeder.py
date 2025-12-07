from ..models.privilege_model import PrivilegeModel
from ..models.privilege_permission_link_model import PrivilegeRouteLinkModel
from ..services.privilege_service import PrivilegeService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete


class PrivilegeSeeder:
    """
    Seeder for PrivilegeModel to populate initial data.
    """

    @staticmethod
    async def run(session: AsyncSession):
        """
        Run the seeder to insert sample data into the database.
        """
        records = [
            {
                "access": "read",
            },
            {
                "access": "write",
            },
            {
                "access": "update",
            },
            {
                "access": "delete",
            },
        ]

        # Insert the data into the database using a loop
        for record in records:
            await PrivilegeService.create(record, session)

    @staticmethod
    async def delete_all(session: AsyncSession):
        """
        Delete all privileges from the database.
        """
        try:
            await session.execute(delete({PrivilegeRouteLinkModel, PrivilegeModel}))
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
