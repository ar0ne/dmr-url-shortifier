import uuid

from django.db import transaction

from apps.links.domain.entities import ShortURLEntity
from apps.links.infrastructure.mapper import ShortURLModelMapper
from apps.links.infrastructure.repositories import DjangoShortURLRepository
from apps.links.infrastructure.services import URLShortifierService


# TODO: from configs
MAX_SHORT_CODE_LENGTH = 25
LATEST_LINKS_SIZE = 10


def get_url_shortifier_service() -> URLShortifierService:
    return URLShortifierService(
        repository=DjangoShortURLRepository(mapper=ShortURLModelMapper()),
        max_length=MAX_SHORT_CODE_LENGTH,
        trx_context_manager=transaction.atomic,
    )


def create_short_url(
    original_url: str, created_by: uuid.UUID | None = None
) -> ShortURLEntity:
    service = get_url_shortifier_service()
    return service.shortify(original_url=original_url, created_by=created_by)


def get_by_code_and_increment_views(short_code: str) -> ShortURLEntity:
    service = get_url_shortifier_service()
    return service.increment_views(short_code)


def get_latest_links(size: int = LATEST_LINKS_SIZE) -> list[ShortURLEntity]:
    service = get_url_shortifier_service()
    return service.get_latest(size)
