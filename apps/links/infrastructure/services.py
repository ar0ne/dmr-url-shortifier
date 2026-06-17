import secrets
import string
import uuid

from django.db import transaction
from django.db.models import F, QuerySet

from apps.links.domain.entities import ShortedURLEntity
from apps.links.domain.exceptions import ShortURLCollisionError
from apps.links.infrastructure.models import ShortURLModel

# __all__ = [
#     "shortify_url",
#     "get_and_increment_url",
#     "get_latest_links",
# ]

from apps.links.domain.interfaces import IURLShortifyService, IURLShortifyRepository, ITransactionContext


class SimpleUrlShortifierService(IURLShortifyService):
    CHARACTERS = string.ascii_letters + string.digits
    LATEST_SIZE = 10

    def __init__(self, repository: IURLShortifyRepository, trx_context_manager: ITransactionContext, max_length: int) -> None:
        self._repository = repository
        self._max_length = max_length
        self._trx_atomic = trx_context_manager

    def create_short_url(self, /, *, original_url: str, created_by: uuid.UUID | None = None) -> ShortedURLEntity:
        while True:
            entity = ShortedURLEntity(
                original_url=original_url,
                short_code=self._random_string(),
                views_count=0,
                create_by_id=created_by,
            )
            with self._trx_atomic():
                try:
                    return self._repository.save(entity)
                except ShortURLCollisionError:
                    continue

    def _random_string(self) -> str:
        """
        Just creates random string. Instead, we could hash original URL.
        """
        return "".join((secrets.choice(self.CHARACTERS) for _ in range(self._max_length)))


# def get_and_increment_url(key: str) -> ShortUrlModel:
#     assert key, "Link key should be not empty"
#     with transaction.atomic():
#         url = (
#               ShortUrlModel.objects
#                 # no_key works only for PostgreSQL at the moment
#                 .select_for_update(of=("self",), no_key=True)
#                 .get(key=key)
#         )
#         url.hits = F("hits") + 1
#         url.save(update_fields=["hits"])
#         return url
#
#
# def get_latest_links() -> QuerySet:
#     return ShortUrlModel.objects.all()[:LATEST_SIZE]
