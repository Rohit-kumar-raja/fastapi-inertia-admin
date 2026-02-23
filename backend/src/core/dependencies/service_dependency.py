from typing import AsyncGenerator, Type, TypeVar
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from  . import get_db
from ..common.uow.uow import AsyncUnitOfWork

S = TypeVar("S")
R = TypeVar("R")


def get_service(service_class: Type[S], repo_class: Type[R]):
    """
    Creates a FastAPI dependency that yields a fully initialized service
    wrapped in a Unit of Work transaction boundary.
    """

    async def dependency(
        session: AsyncSession = Depends(get_db),
    ) -> AsyncGenerator[S, None]:
        # 1. The transaction starts dynamically with the provided repo_class
        async with AsyncUnitOfWork(session, repo_class) as uow:
            # 2. Instantiate the service with the UoW
            service = service_class(uow=uow)
            # 3. Yield it to the FastAPI route
            yield service
        # 4. The route finishes, and the AsyncUnitOfWork __aexit__ triggers (commit/rollback)

    return dependency
