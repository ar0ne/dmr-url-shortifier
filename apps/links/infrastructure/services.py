import logging
import secrets
import string
import uuid

from apps.links.domain.entities import ShortURLEntity
from apps.links.domain.exceptions import ShortURLCollisionError

logger = logging.getLogger(__name__)

__all__ = [
    "SimpleUrlShortifierService",
]

from apps.links.domain.interfaces import (
    IShortifyURLService,
    IShortifyURLRepository,
    ITransactionContext,
)


class SimpleUrlShortifierService(IShortifyURLService):
    CHARACTERS = string.ascii_letters + string.digits

    def __init__(
        self,
        repository: IShortifyURLRepository,
        trx_context_manager: ITransactionContext,
        max_length: int,
    ) -> None:
        self._repository = repository
        self._max_length = max_length
        self._trx_atomic = trx_context_manager

    def shortify(
        self, /, *, original_url: str, created_by: uuid.UUID | None = None
    ) -> ShortURLEntity:
        """
        Shortifies original URL and creates new record in DB.
        """
        while True:
            entity = ShortURLEntity(
                original_url=original_url,
                short_code=self._random_string(),
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

    def _random_string(self) -> str:
        """
        Just creates random string. Instead, we could hash original URL.
        """
        return "".join(
            (secrets.choice(self.CHARACTERS) for _ in range(self._max_length))
        )


# def get_latest_links() -> QuerySet:
#     return ShortUrlModel.objects.all()[:LATEST_SIZE]
