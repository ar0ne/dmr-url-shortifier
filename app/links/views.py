import pydantic
from dmr import Controller, Body
from dmr.plugins.pydantic import PydanticSerializer


class ShortUrlModel(pydantic.BaseModel):
    name: str
    url: str


class ShortUrlCreateModel(pydantic.BaseModel):
    url: str


class LinkController(Controller[PydanticSerializer]):
    def get(self) -> ShortUrlModel:
        return ShortUrlModel(name="foo", url="bar")

    def post(self, parsed_body: Body[ShortUrlCreateModel]) -> ShortUrlModel:
        return ShortUrlModel()