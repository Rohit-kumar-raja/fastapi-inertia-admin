from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from .settings import settings

engine = create_async_engine(settings.APP_DATABASE_URL, echo=False)
# Synchronous engine for migrations or sync tasks (if needed)
sync_engine = create_engine(settings.APP_DATABASE_URL.replace("asyncpg", "psycopg2"), echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False, class_=AsyncSession, autocommit=False
)


class Base(DeclarativeBase):
    pass
