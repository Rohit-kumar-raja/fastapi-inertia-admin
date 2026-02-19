import asyncio

# from .route_seeder import PermissionSeeder
# from .role_seeder import RoleSeeder
from .user_seeder import UserSeeder
from core.config.database import AsyncSessionLocal

seeders = [ UserSeeder]


async def run_seeders():
    async with AsyncSessionLocal() as session:
        for seeder in seeders:
            await seeder.run(session)


asyncio.run(run_seeders())
