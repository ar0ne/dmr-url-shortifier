import uuid
from typing import final

from pydantic.dataclasses import dataclass


@final
@dataclass(frozen=True, kw_only=True)
class ShortedURLEntity:
    original_url: str
    short_code: str
    views_count: int
    create_by_id: uuid.UUID | None
