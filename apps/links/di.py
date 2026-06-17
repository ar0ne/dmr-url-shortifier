from django.db import transaction

from apps.links.domain.interfaces import IStringGenerator, IShortifyURLRepository
from apps.links.infrastructure.mapper import ShortURLModelMapper
from apps.links.infrastructure.repositories import DjangoShortURLRepository
from apps.links.infrastructure.services import (
    RandomStringGenerator,
    URLShortifierService,
)

# TODO: from configs
MAX_SHORT_CODE_LENGTH = 25


def get_repository() -> IShortifyURLRepository:
    return DjangoShortURLRepository(_mapper=ShortURLModelMapper())


def get_string_generator() -> IStringGenerator:
    return RandomStringGenerator(_max_length=MAX_SHORT_CODE_LENGTH)


def get_url_shortifier_service() -> URLShortifierService:
    return URLShortifierService(
        _repository=get_repository(),
        _trx_atomic=transaction.atomic,
        _generator=get_string_generator(),
    )
