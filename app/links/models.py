from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import DO_NOTHING
from django.utils.translation import gettext_lazy as _

class ShortUrl(models.Model):
    key = models.CharField(
        verbose_name=_("URL key"),
        help_text=_("Unique key for shortified URL"),
        max_length=15, unique=True, db_index=True,
    )
    target_url = models.URLField(
        verbose_name=_("Target URL"), blank=False
    )
    hits = models.PositiveIntegerField(
        verbose_name=_("Hits"),
        help_text=_("Total times the URL was requested"),
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=DO_NOTHING)

    class Meta:
        verbose_name = "Short URL"
        verbose_name_plural = "Short URLs"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["key"])
        ]