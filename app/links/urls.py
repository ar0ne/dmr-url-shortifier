from dmr.routing import Router, path

from app.links.views import LinkController

router = Router(
    "v1/",
    [
        path(
            'links/',
            LinkController.as_view(),
            name='links',
        ),
    ],
)