from rest_framework import serializers

from .models import Catalog, CatalogItem


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ["id", "code", "name"]


class CatalogItemSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source="item_code", max_length=100)
    value = serializers.CharField(source="item_value", max_length=300)

    class Meta:
        model = CatalogItem
        fields = ["code", "value"]
