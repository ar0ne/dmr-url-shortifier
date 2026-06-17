import uuid

from django.db import transaction

from apps.links.domain.entities import ShortURLEntity
from apps.links.infrastructure.mapper import ShortURLModelMapper
from apps.links.infrastructure.repositories import DjangoShortURLRepository
from apps.links.infrastructure.services import SimpleUrlShortifierService


def get_create_url_shortifier_service() -> SimpleUrlShortifierService:
    return SimpleUrlShortifierService(
        repository=DjangoShortURLRepository(mapper=ShortURLModelMapper()),
        max_length=25,  # TODO: from configs
        trx_context_manager=transaction.atomic,
    )


def create_short_url(
    original_url: str, created_by: uuid.UUID | None = None
) -> ShortURLEntity:
    service = get_create_url_shortifier_service()
    return service.create_short_url(original_url=original_url, created_by=created_by)
