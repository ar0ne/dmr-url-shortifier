from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import DO_NOTHING
from django.utils.translation import gettext_lazy as _

__all__ = [
    "ShortUrl",
]


class ShortUrl(models.Model):
    key = models.CharField(
        verbose_name=_("URL key"),
        help_text=_("Unique key for shortified URL"),
        max_length=15,
        unique=True,
        db_index=True,  # used as unique public identifier
    )
    target_url = models.URLField(
        verbose_name=_("Target URL"),
        blank=False,
    )
    hits = models.PositiveIntegerField(
        verbose_name=_("Hits"),
        help_text=_("Total times the URL was requested"),
        null=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=False,  # used to speed up getting the latest
    )
    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        related_name="+",
        on_delete=DO_NOTHING,
        db_index=False,  # partial index defined in indexes
    )

    class Meta:
        verbose_name = "Short URL"
        verbose_name_plural = "Short URLs"

        ordering = ["-created_at"]

        indexes = [
            models.Index(
                name="links_shorturl_key_idx",
                fields=["key"],
            ),
            models.Index(
                name="links_shorturl_created_at_idx",
                fields=["created_at"],
            ),
            models.Index(
                name="links_shorturl_created_by_idx",
                fields=("created_by_id",),
                condition=models.Q(created_by_id__isnull=False)
            )
        ]
