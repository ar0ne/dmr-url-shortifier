from pydantic import HttpUrl

from apps.links.api.schemes import ShortedURLScheme
from apps.links.domain.entities import ShortedURLEntity


class ShortURLDtoMapper:

    @staticmethod
    def map(entity: ShortedURLEntity) -> ShortedURLScheme:
        return ShortedURLScheme(
            key=entity.short_code,
            target_url=HttpUrl(entity.original_url),
            hits=entity.views_count,
            # created_at=None,
        )