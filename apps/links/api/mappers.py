from apps.links.api.schemes import ShortedURLScheme
from apps.links.domain.entities import ShortURLEntity


class ShortURLDtoMapper:
    @staticmethod
    def map(entity: ShortURLEntity) -> ShortedURLScheme:
        return ShortedURLScheme(
            short_code=entity.short_code,
            target_url=entity.original_url,
            views=entity.views_count,
            created_at=entity.created_at,
            created_by=entity.create_by_id,
        )
