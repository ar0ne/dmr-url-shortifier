from datetime import datetime
from typing import Self

import pydantic
from pydantic import HttpUrl

from apps.links.domain.entities import ShortedURLEntity


class ShortedURLScheme(pydantic.BaseModel):
    key: str
    target_url: HttpUrl
    hits: int
    created_at: datetime

    # @classmethod
    # def from_model(cls, obj: ShortedUrlEntity) -> Self:
    #     return cls(
    #         key=obj.key,
    #         target_url=obj.target_url,
    #         hits=obj.hits,
    #         created_at=obj.created_at,
    #     )


class ShortedURLListScheme(pydantic.BaseModel):
    data: list[ShortedURLScheme]


class CreateShortURLScheme(pydantic.BaseModel):
    target_url: HttpUrl

