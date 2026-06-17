from django.db import IntegrityError

from apps.links.domain.entities import ShortURLEntity
from apps.links.domain.exceptions import ShortURLCollisionError, ShourtURLNotFound
from apps.links.domain.interfaces import IURLShortifyRepository
from apps.links.infrastructure.mapper import ShortURLModelMapper
from apps.links.infrastructure.models import ShortURLModel


class DjangoShortURLRepository(IURLShortifyRepository):
    def __init__(self, mapper: ShortURLModelMapper) -> None:
        self._mapper = mapper

    def save(self, entity: ShortURLEntity) -> ShortURLEntity:
        try:
            model = ShortURLModel.objects.create(
                key=entity.short_code,
                target_url=entity.original_url,
                hits=entity.views_count,
                created_by=entity.create_by_id,
            )
            return self._mapper.from_model(model)
        except IntegrityError as exc:
            raise ShortURLCollisionError(exc)

    def get_by_code(self, short_code: str) -> ShortURLEntity:
        try:
            model = ShortURLModel.objects.get(key=short_code)
            return self._mapper.from_model(model)
        except ShortURLModel.DoesNotExist as exc:
            raise ShourtURLNotFound(exc)
