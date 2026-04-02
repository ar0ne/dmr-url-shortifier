import logging
from http import HTTPStatus
from typing import Self

import pydantic
from django.db import transaction, IntegrityError
from dmr import Controller, Body, APIError, ResponseSpec
from dmr.errors import ErrorType
from dmr.plugins.pydantic import PydanticSerializer
from pydantic import Field

from .models import ShortUrl
from .services import shortify

logger = logging.getLogger(__name__)


class LinkModel(pydantic.BaseModel):
    name: str
    target_url: str

    @classmethod
    def from_model(cls, obj: ShortUrl) -> Self:
        return cls(
            name=obj.name,
            target_url=obj.target_url
        )


class LinkListModel(pydantic.BaseModel):
    data: list[LinkModel]


class LinkCreateModel(pydantic.BaseModel):
    target_url: str = Field(..., min_length=3, max_length=200)


class DetailLinkController(Controller[PydanticSerializer]):
    responses = (
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.NOT_FOUND,
        ),
    )

    # TODO: 404 is not documented
    def get(self) -> LinkModel:
        name = self.kwargs['name']
        with transaction.atomic():
            try:
                url = ShortUrl.objects.get(name=name)
                return LinkModel.from_model(url)
            except ShortUrl.DoesNotExist:
                raise APIError(
                    self.format_error(
                        f"Unable to find link with {name=}",
                        error_type=ErrorType.not_found
                    ),
                    status_code=HTTPStatus.NOT_FOUND
                )


def get_user(request):
    if request.user.is_authenticated:
        return request.user
    return None


class LinkController(Controller[PydanticSerializer]):

    def get(self) -> LinkListModel:
        latest = ShortUrl.objects.all()[:10]
        return LinkListModel(data=map(LinkModel.from_model, latest))

    def post(self, parsed_body: Body[LinkCreateModel]) -> LinkModel:
        while True:
            short_name = shortify(parsed_body.target_url)
            with transaction.atomic():
                try:
                    link = ShortUrl.objects.create(
                        name=short_name,
                        target_url=parsed_body.target_url,
                        created_by=get_user(self.request),
                        hits=0
                    )
                    return LinkModel.from_model(link)
                except IntegrityError as err:
                    logger.debug("Unable to save link due to DB integrity error", err)
                    # short url with this name already exists, try again with another name
                    continue
