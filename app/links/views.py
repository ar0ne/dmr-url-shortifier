import logging
from datetime import datetime
from http import HTTPStatus
from typing import override, Self

import pydantic
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from dmr import Controller, Body, APIError, ResponseSpec
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.plugins.pydantic import PydanticSerializer
from pydantic import Field, HttpUrl

from .models import ShortUrl
from .services import shortify, get_and_increment_url

logger = logging.getLogger(__name__)


class LinkModel(pydantic.BaseModel):
    key: str
    target_url: HttpUrl
    hits: int
    created_at: datetime

    @classmethod
    def from_model(cls, obj: ShortUrl) -> Self:
        return cls(
            key=obj.key,
            target_url=obj.target_url,
            hits=obj.hits,
            created_at=obj.created_at
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
        key = self.kwargs['key']
        try:
            url = get_and_increment_url(key)
            return LinkModel.from_model(url)
        except ShortUrl.DoesNotExist:
            raise APIError(
                self.format_error(
                    f"Unable to find link with {key=}",
                    error_type=ErrorType.not_found
                ),
                status_code=HTTPStatus.NOT_FOUND
            )


def get_user(request):
    if request.user.is_authenticated:
        return request.user
    return None


class LinkController(Controller[PydanticSerializer]):
    responses = (
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.BAD_REQUEST,
        ),
    )

    def get(self) -> LinkListModel:
        latest = ShortUrl.objects.all()[:10]
        return LinkListModel(data=map(LinkModel.from_model, latest))

    def post(self, parsed_body: Body[LinkCreateModel]) -> LinkModel:
        while True:
            key = shortify(parsed_body.target_url)
            with transaction.atomic():
                try:
                    link = ShortUrl.objects.create(
                        key=key,
                        target_url=parsed_body.target_url,
                        created_by=get_user(self.request),
                        hits=0
                    )
                    return LinkModel.from_model(link)
                except IntegrityError as err:
                    logger.debug("Unable to save link due to DB integrity error", err)
                    # url with this key already exists, auto retry with another key
                    continue

    @override
    def handle_error(
            self,
            endpoint: Endpoint,
            controller: Controller[PydanticSerializer],
            exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, pydantic.ValidationError):
            return self.to_response(
                self.format_error('Validation error: {}'.format(exc.errors()[0]['msg'])),
                status_code=HTTPStatus.BAD_REQUEST,
            )
        return super().handle_error(endpoint, controller, exc)
