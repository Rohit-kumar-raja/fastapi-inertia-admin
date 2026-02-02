from ..services.role_service import RoleService
from ..services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete
from core.security.models.user_model import UserModel


class UserSeeder:
    """
    Seeder for UserModel to populate initial data.
    """

    @staticmethod
    async def run(session: AsyncSession):
        """
        Run the seeder to insert sample data into the database.
        """
        # Sample data to be inserted into the database
        records = [
            {
                "username": "admin",
                "email": "admin@conquer.dev",
                "phone": "1234567890",
                "is_superuser": True,
                "is_active": True,
                "password": "Admin@1234",  # Replace with actual hashed password
            },
          
            
        ]

        # Insert the data into the database using a loop
        for record in records:
            role_services = await RoleService.get_all(session=session)
            record["role_ids"] = [role.id for role in role_services]
            await UserService.create(record, session=session)

    @staticmethod
    async def delete_all(session: AsyncSession):
        """
        Delete all users from the database.
        """
        try:
            await session.execute(delete(UserModel))
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
