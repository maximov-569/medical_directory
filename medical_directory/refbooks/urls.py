from django.urls import path, include
from rest_framework import routers

from .views import (
    CatalogViewSet,
    CatalogItemViewSet,
)

router_v1 = routers.DefaultRouter()
router_v1.register(r"", CatalogViewSet)

urlpatterns = [
    path("<int:catalog_id>/elements/", CatalogItemViewSet.as_view({"get": "list"})),
    path(
        "<int:catalog_id>/check_element/",
        CatalogItemViewSet.as_view({"get": "retrieve"}),
    ),
    path("", include(router_v1.urls)),
]
