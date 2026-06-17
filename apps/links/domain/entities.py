import uuid
from datetime import datetime
from typing import final

from pydantic.dataclasses import dataclass


@final
@dataclass(frozen=True, kw_only=True)
class ShortURLEntity:
    original_url: str
    short_code: str
    views_count: int
    created_at: datetime | None = None
    create_by_id: uuid.UUID | None = None
