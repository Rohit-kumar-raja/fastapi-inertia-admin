from typing import Any, Dict, Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

TRepo = TypeVar("TRepo")
R = TypeVar("R")


class AsyncUnitOfWork(Generic[TRepo]):
    def __init__(self, session: AsyncSession, primary_repo_class: Type[TRepo]):
        self.session = session
        self.primary_repo_class = primary_repo_class
        self._instantiated_repos: Dict[Type[Any], Any] = {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        # Automatically commits if no errors, rolls back if an exception occurs
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()

    @property
    def repo(self) -> TRepo:
        """Returns the primary repository with IDE type hinting."""
        return self.get_repo(self.primary_repo_class)

    def get_repo(self, repo_class: Type[R]) -> R:
        """Dynamically instantiates any repository on demand injected with the current session."""
        if repo_class not in self._instantiated_repos:
            self._instantiated_repos[repo_class] = repo_class(self.session)
        return self._instantiated_repos[repo_class]
