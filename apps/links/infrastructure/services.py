import logging
import secrets
import string
import uuid
from dataclasses import dataclass
from typing import final

from apps.links.domain.entities import ShortURLEntity
from apps.links.domain.exceptions import ShortURLCollisionError

logger = logging.getLogger(__name__)

__all__ = [
    "URLShortifierService",
    "RandomStringGenerator",
]

from apps.links.domain.interfaces import (
    IShortifyURLService,
    IShortifyURLRepository,
    ITransactionContext,
    IStringGenerator,
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class URLShortifierService(IShortifyURLService):
    _repository: IShortifyURLRepository
    _trx_atomic: ITransactionContext
    _generator: IStringGenerator

    def shortify(
        self, /, *, original_url: str, created_by: uuid.UUID | None = None
    ) -> ShortURLEntity:
        """
        Shortifies original URL and creates new record in DB.
        """
        while True:
            entity = ShortURLEntity(
                original_url=original_url,
                short_code=self._generator(seed=original_url),
                views_count=0,
                create_by_id=created_by,
            )
            with self._trx_atomic():
                try:
                    return self._repository.save(entity)
                except ShortURLCollisionError as exc:
                    logger.info("Short URL collision", exc)
                    continue
        assert False, "unreachable"

    def increment_views(self, short_code: str) -> ShortURLEntity:
        with self._trx_atomic():
            return self._repository.increase_views(short_code)

    def get_latest(self, size: int = 10) -> list[ShortURLEntity]:
        return self._repository.get_latest(size)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class RandomStringGenerator:
    CHARACTERS = string.ascii_letters + string.digits

    _max_length: int

    """
    Just creates random string. Instead, we could hash original URL.
    """

    def __call__(self, /, *, seed: str) -> str:
        return "".join(
            (secrets.choice(self.CHARACTERS) for _ in range(self._max_length))
        )
