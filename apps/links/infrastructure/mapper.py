from pydantic.dataclasses import dataclass

from apps.links.domain.entities import ShortURLEntity
from apps.links.infrastructure.models import ShortURLModel


@dataclass(frozen=True, slots=True)
class ShortURLModelMapper:
    @staticmethod
    def from_model(model: ShortURLModel) -> ShortURLEntity:
        return ShortURLEntity(
            original_url=model.target_url,
            short_code=model.key,
            views_count=model.hits,
            create_by_id=model.created_by,
            created_at=model.created_at,
        )
