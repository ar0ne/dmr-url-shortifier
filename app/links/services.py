import secrets
import string

from django.db import transaction
from django.db.models import F, QuerySet

from app.links.models import ShortUrl

__all__ = [
    "shortify_url",
    "get_and_increment_url",
    "get_latest_links",
]

CHARACTERS = string.ascii_letters + string.digits
LATEST_SIZE = 10


def shortify_url(_: str, size: int = 5) -> str:
    """
    Just create random string.
    Instead, we could hash original URL.
    """
    return "".join((secrets.choice(CHARACTERS) for _ in range(size)))


def get_and_increment_url(key: str) -> ShortUrl:
    assert key, "Link key should be not empty"
    with transaction.atomic():
        url = (
              ShortUrl.objects
                .select_for_update(of=("self",), no_key=True)
                .get(key=key)
        )
        url.hits = F("hits") + 1
        url.save(update_fields=["hits"])
        return url


def get_latest_links() -> QuerySet:
    return ShortUrl.objects.all()[:LATEST_SIZE]
