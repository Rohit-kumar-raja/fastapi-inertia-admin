from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete

from core.common.uow.uow import AsyncUnitOfWork
from core.security.models.user_model import UserModel
from core.security.repositories.user_repository import UserRepository
from core.security.repositories.role_repository import RoleRepository
from core.security.services.user_service import UserService
from core.security.services.role_service import RoleService


class UserSeeder:
    """
    Seeder for UserModel to populate initial data.
    """

    @staticmethod
    async def run(session: AsyncSession):
        """
        Run the seeder to insert sample data into the database.
        """
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

        async with AsyncUnitOfWork(session, RoleRepository) as role_uow:
            role_service = RoleService(role_uow)
            roles = await role_service.get_all()

        async with AsyncUnitOfWork(session, UserRepository) as user_uow:
            user_service = UserService(user_uow)
            for record in records:
                # Add role IDs to the user record
                record["role_ids"] = [str(role.id) for role in roles]
                await user_service.create(record)

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
