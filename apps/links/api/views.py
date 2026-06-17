import logging
import uuid
from http import HTTPStatus
from typing import override

import pydantic
from django.http import HttpResponse
from dmr import Body, Controller, ResponseSpec, APIError
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.plugins.pydantic import PydanticSerializer

from apps.links.api.mappers import ShortURLDtoMapper
from apps.links.api.schemes import (
    CreateShortURLScheme,
    ShortedURLScheme,
    ShortedURLListScheme,
)
from apps.links.domain.exceptions import ShortURLNotFound
from apps.links.infrastructure.use_cases import (
    create_short_url,
    get_by_code_and_increment_views,
    get_latest_links,
)

logger = logging.getLogger(__name__)

__all__ = [
    "LinkDetailsController",
    "CreateListLinkController",
]


def get_user_id(request) -> uuid.UUID | None:
    if request.user.is_authenticated:
        return request.user.id
    return None


class LinkDetailsController(Controller[PydanticSerializer]):
    responses = (
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.NOT_FOUND,
        ),
    )

    # TODO: 404 is not documented
    def get(self) -> ShortedURLScheme:
        short_code = self.kwargs["short_code"]
        try:
            entity = get_by_code_and_increment_views(short_code)
            return ShortURLDtoMapper.map(entity)
        except ShortURLNotFound as exc:
            raise APIError(
                self.format_error(
                    f"Unable to find URL with {short_code=}",
                    error_type=ErrorType.not_found,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )


class CreateListLinkController(Controller[PydanticSerializer]):
    responses = (
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.BAD_REQUEST,
        ),
    )

    def get(self) -> ShortedURLListScheme:
        return ShortedURLListScheme(
            results=list(map(ShortURLDtoMapper.map, get_latest_links()))
        )

    def post(self, parsed_body: Body[CreateShortURLScheme]) -> ShortedURLScheme:
        entity = create_short_url(
            original_url=str(parsed_body.target_url),
            created_by=get_user_id(self.request),
        )
        return ShortURLDtoMapper.map(entity)

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[PydanticSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, pydantic.ValidationError):
            return self.to_response(
                self.format_error(
                    "Validation error: {}".format(exc.errors()[0]["msg"])
                ),
                status_code=HTTPStatus.BAD_REQUEST,
            )
        return super().handle_error(endpoint, controller, exc)
