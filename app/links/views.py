import pydantic
from dmr import Controller, Body
from dmr.plugins.pydantic import PydanticSerializer


class ShortUrlModel(pydantic.BaseModel):
    name: str
    target_url: str


class ShortUrlCreateModel(pydantic.BaseModel):
    target_url: str


class LinkController(Controller[PydanticSerializer]):
    def get(self) -> ShortUrlModel:
        return ShortUrlModel(name="foo", target_url="bar")

    def post(self, parsed_body: Body[ShortUrlCreateModel]) -> ShortUrlModel:
        return ShortUrlModel()
