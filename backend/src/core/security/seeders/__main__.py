import asyncio

from .role_seeder import RoleSeeder
from .route_seeder import RouteSeeder
from .user_seeder import UserSeeder
from .privilege_seeder import PrivilegeSeeder
from core.config.database import AsyncSessionLocal

seeders = [PrivilegeSeeder, RouteSeeder, RoleSeeder, UserSeeder]


async def run_seeders():
    async with AsyncSessionLocal() as session:
        for seeder in seeders:
            await seeder.run(session)


asyncio.run(run_seeders())
