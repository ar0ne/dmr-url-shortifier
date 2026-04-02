from dmr.routing import Router, path

from .views import DetailShortUrlController, LatestLinkController

router = Router(
    "api/v1/",
    [
        path('links/<int:link_id>', DetailShortUrlController.as_view(), name='link-details'),
        path('links/', LatestLinkController.as_view(), name='link-list'),
    ],
)