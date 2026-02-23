from typing import Any, Generic, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model_class: Type[ModelType]):
        self.session = session
        self.model_class = model_class

    async def get_by_id(self, id: Any) -> ModelType | None:
        return await self.session.get(self.model_class, id)

    async def get_all(self) -> list[ModelType]:
        result = await self.session.execute(select(self.model_class))
        return result.scalars().all()

    async def add(self, instance: ModelType) -> None:
        self.session.add(instance)
        await self.session.flush()

    async def update(self, instance: ModelType) -> None:
        self.session.add(instance)
        await self.session.flush()

    async def delete(self, instance: ModelType) -> None:
        await self.session.delete(instance)
        await self.session.flush()
