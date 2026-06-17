import uuid

from apps.links.di import get_url_shortifier_service
from apps.links.domain.entities import ShortURLEntity

# TODO: from configs
LATEST_LINKS_SIZE = 10


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
