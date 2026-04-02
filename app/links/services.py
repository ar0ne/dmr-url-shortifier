import secrets
import string

from django.db import transaction
from django.db.models import F

from app.links.models import ShortUrl

CHARACTERS = string.ascii_letters + string.digits


def shortify(_: str, size: int = 5) -> str:
    """
    Create random string.
    Instead, we could hash original URL.
    """
    return ''.join((secrets.choice(CHARACTERS) for _ in range(size)))

def get_and_increment_url(key: str) -> ShortUrl:
    assert key, "Link key should be not empty"
    with transaction.atomic():
        url = ShortUrl.objects.select_for_update().get(key=key)
        url.hits = F("hits") + 1
        url.save(update_fields=['hits'])
        return url