import uuid
from abc import abstractmethod
from contextlib import AbstractContextManager
from typing import Protocol

from apps.links.domain.entities import ShortURLEntity


class IShortifyURLService(Protocol):
    _max_length: int

    def shortify(
        self, /, *, original_url: str, created_by: uuid.UUID | None = None
    ) -> ShortURLEntity: ...


class IShortifyURLRepository(Protocol):
    def save(self, entity: ShortURLEntity) -> ShortURLEntity: ...

    def get_by_code(self, short_code: str) -> ShortURLEntity: ...


class ITransactionContext(Protocol):
    @abstractmethod
    def __call__(self) -> AbstractContextManager[None]:
        """Return a context manager that wraps code in an atomic transaction."""
        ...
