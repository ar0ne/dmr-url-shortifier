from dmr.routing import Router, path

from .views import CreateListLinkController, LinkDetailsController

router = Router(
    "api/v1/",
    [
        path(
            "links/<str:short_code>",
            LinkDetailsController.as_view(),
            name="link-details",
        ),
        path("links/", CreateListLinkController.as_view(), name="link-list"),
    ],
)
