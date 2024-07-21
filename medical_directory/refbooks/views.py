from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.status import HTTP_404_NOT_FOUND

from .serializers import (
    CatalogSerializer,
    CatalogItemSerializer,
)
from .models import Catalog, CatalogItem, CatalogVersion

from .schemas import (
    catalog_view_set_list,
    catalog_item_view_set_list,
    catalog_item_view_set_retrieve,
)


class CatalogViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    API endpoint that allows catalogs to be viewed.
    """

    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        date = self.request.query_params.get("date")
        if date:
            return Catalog.objects.filter(
                id__in=CatalogVersion.objects.filter(
                    version_start_date__gte=date
                ).values_list("catalog_id", flat=True)
            )
        return self.queryset

    @swagger_auto_schema(
        manual_parameters=catalog_view_set_list["manual_parameters"],
        responses=catalog_view_set_list["responses"],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"refbooks": serializer.data})


class CatalogItemViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    """
    API endpoint that allows catalog items to be viewed or edited.
    """

    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        catalog_id = self.kwargs.get("catalog_id")
        version = self.request.query_params.get("version")

        if version:
            return CatalogItem.objects.filter(
                catalog_version_id__catalog_id=catalog_id,
                catalog_version_id__version=version,
            )

        return CatalogItem.objects.filter(
            catalog_version_id=CatalogVersion.objects.filter(catalog_id=catalog_id)
            .order_by("-version_start_date")[:1]
            .values_list("id", flat=True)
        )

    @swagger_auto_schema(
        manual_parameters=catalog_item_view_set_list["manual_parameters"],
        responses=catalog_item_view_set_list["responses"],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"elements": serializer.data})

    def get_object(self):
        catalog_id = self.kwargs.get("catalog_id")
        version = self.request.query_params.get("version")
        value = self.request.query_params.get("value")
        code = self.request.query_params.get("code")

        if version:
            return CatalogItem.objects.filter(
                catalog_version_id__catalog_id=catalog_id,
                item_value=value,
                item_code=code,
                catalog_version_id__version=version,
            )

        return CatalogItem.objects.filter(
            catalog_version_id=CatalogVersion.objects.filter(catalog_id=catalog_id)
            .order_by("-version_start_date")[:1]
            .values_list("id", flat=True),
            item_value=value,
            item_code=code,
        )

    @swagger_auto_schema(
        manual_parameters=catalog_item_view_set_retrieve["manual_parameters"],
        responses=catalog_item_view_set_retrieve["responses"],
    )
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"status": "Element not found"}, status=HTTP_404_NOT_FOUND)
