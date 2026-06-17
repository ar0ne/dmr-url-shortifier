import uuid
from datetime import datetime

import pydantic
from pydantic import HttpUrl


class ShortedURLScheme(pydantic.BaseModel):
    short_code: str
    target_url: str
    views: int
    created_at: datetime | None
    created_by: uuid.UUID | None = None


class ShortedURLListScheme(pydantic.BaseModel):
    data: list[ShortedURLScheme]


class CreateShortURLScheme(pydantic.BaseModel):
    target_url: HttpUrl
