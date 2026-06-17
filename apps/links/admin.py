from django.contrib import admin

from apps.links.infrastructure.models import ShortURLModel


@admin.register(ShortURLModel)
class ShortLinkAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "key",
        "target_url",
    )