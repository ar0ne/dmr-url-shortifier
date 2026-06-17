from apps.links.domain.entities import ShortedURLEntity
from apps.links.infrastructure.models import ShortURLModel


class ShortURLModelMapper:

    @staticmethod
    def from_model(model: ShortURLModel) -> ShortedURLEntity:
        return ShortedURLEntity(
            original_url=model.target_url,
            short_code=model.key,
            views_count=model.hits,
            create_by_id=model.created_by,
        )

    @staticmethod
    def from_entity(entity: ShortedURLEntity) -> ShortURLModel:
        return ShortURLModel(
            key=entity.short_code,
            target_url=entity.original_url,
            hits=entity.views_count,
            created_by=entity.create_by_id,
        )