from django.contrib import admin
from django.urls import include, path
from dmr.openapi import build_schema
from dmr.openapi.views import OpenAPIJsonView, SwaggerView

from app.links.routes import router as links_router_v1

schema = build_schema(links_router_v1)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include((links_router_v1.urls, "links-app"), namespace="links")),
    path("docs/openapi.json/", OpenAPIJsonView.as_view(schema), name="openapi"),
    path("docs/swagger/", SwaggerView.as_view(schema), name="swagger"),
]
