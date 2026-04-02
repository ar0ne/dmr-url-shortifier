from django.contrib import admin
from django.urls import path
from django.urls import include

from app.links.urls import router as links_router_v1

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((links_router_v1.urls, 'links-app'), namespace='links')),
]
