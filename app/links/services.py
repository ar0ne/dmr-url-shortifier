import secrets
import string

CHARACTERS = string.ascii_letters + string.digits


def shortify(_: str, size: int = 5) -> str:
    """
    Create random string.
    Instead, we could hash original URL.
    """
    return ''.join((secrets.choice(CHARACTERS) for _ in range(size)))
