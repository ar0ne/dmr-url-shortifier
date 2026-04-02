from http import HTTPStatus

import pydantic
from dmr import Controller, Body, APIError
from dmr.plugins.pydantic import PydanticSerializer
from pydantic_core import ErrorType


class ShortUrlModel(pydantic.BaseModel):
    name: str
    target_url: str


class ShortUrlListModel(pydantic.BaseModel):
    data: list[ShortUrlModel]


class ShortUrlCreateModel(pydantic.BaseModel):
    target_url: str


class DetailShortUrlController(Controller[PydanticSerializer]):
    def get(self) -> ShortUrlModel:
        if self.kwargs["link_id"] is None:
            raise APIError(
                self.format_error(
                    'Url not found',
                    error_type=ErrorType.user_msg,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )
        return ShortUrlModel(name="foo", target_url="bar")


class LatestLinkController(Controller[PydanticSerializer]):
    def get(self) -> ShortUrlListModel:
        return ShortUrlListModel(data=[ShortUrlModel(name="foo", target_url="bar")])


class LinkCreateController(Controller[PydanticSerializer]):
    def post(self, parsed_body: Body[ShortUrlCreateModel]) -> ShortUrlModel:
        return ShortUrlModel()
