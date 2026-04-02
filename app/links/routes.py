from dmr.routing import Router, path

from .views import DetailLinkController, LinkController

router = Router(
    "api/v1/",
    [
        path('links/<str:name>', DetailLinkController.as_view(), name='link-details'),
        path('links/', LinkController.as_view(), name='link-list'),
    ],
)