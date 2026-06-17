import logging
import uuid
from http import HTTPStatus
from typing import override

import pydantic
from django.http import HttpResponse
from dmr import Body, Controller, ResponseSpec
from dmr.endpoint import Endpoint
from dmr.plugins.pydantic import PydanticSerializer

from apps.links.api.mappers import ShortURLDtoMapper
from apps.links.api.schemes import CreateShortURLScheme, ShortedURLScheme
from apps.links.infrastructure.use_cases import create_short_url

logger = logging.getLogger(__name__)

# __all__ = [
    # "DetailLinkController",
    # "LinkController",
# ]


def get_user_id(request) -> uuid.UUID | None:
    if request.user.is_authenticated:
        return request.user.id
    return None

#
# class DetailLinkController(Controller[PydanticSerializer]):
#     responses = (
#         ResponseSpec(
#             Controller.error_model,
#             status_code=HTTPStatus.NOT_FOUND,
#         ),
#     )
#
#     # TODO: 404 is not documented
#     def get(self) -> LinkModel:
#         key = self.kwargs["key"]
#         try:
#             # 'hits' could be not "the latest", need to write Raw SQL to leverage RETURNING
#             url = get_and_increment_url(key)
#             return LinkModel.from_model(url)
#         except ShortUrl.DoesNotExist:
#             raise APIError(
#                 self.format_error(
#                     f"Unable to find link with {key=}", error_type=ErrorType.not_found
#                 ),
#                 status_code=HTTPStatus.NOT_FOUND,
#             )


class LinkController(Controller[PydanticSerializer]):
    responses = (
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.BAD_REQUEST,
        ),
    )

    # def get(self) -> LinkListModel:
    #     return LinkListModel(data=map(LinkModel.from_model, get_latest_links()))

    def post(self, parsed_body: Body[CreateShortURLScheme]) -> ShortedURLScheme:
        entity = create_short_url(
            original_url=str(parsed_body.target_url),
            created_by=get_user_id(self.request)
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
