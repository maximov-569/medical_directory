from django.contrib import admin
from .models import Catalog, CatalogVersion, CatalogItem


class CatalogVersionInline(admin.TabularInline):
    model = CatalogVersion
    extra = 0


class CatalogAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "name", "current_version", "version_start_date"]
    search_fields = ["code", "name"]
    fields = ["code", "name", "description"]
    inlines = [CatalogVersionInline]

    def current_version(self, obj):
        return (
            obj.catalogversion_set.first().version
            if obj.catalogversion_set.first()
            else None
        )

    def version_start_date(self, obj):
        return (
            obj.catalogversion_set.first().version_start_date
            if obj.catalogversion_set.first()
            else None
        )

    current_version.short_description = "Текущая версия"
    version_start_date.short_description = "Дата начала действия версии"


admin.site.register(Catalog, CatalogAdmin)


class CatalogItemInline(admin.TabularInline):
    model = CatalogItem
    extra = 0
    fields = ["item_code", "item_value"]


class CatalogVersionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "catalog_code",
        "catalog_name",
        "version",
        "version_start_date",
    ]
    search_fields = ["catalog_id__code", "catalog_id__name", "version"]
    list_filter = ["catalog_id__code", "catalog_id__name"]
    inlines = [CatalogItemInline]

    def catalog_name(self, obj):
        return obj.catalog_id.name

    def catalog_code(self, obj):
        return obj.catalog_id.code


admin.site.register(CatalogVersion, CatalogVersionAdmin)


class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ["catalog_version_id", "item_code", "item_value"]
    search_fields = ["catalog_version_id__catalog_id__code", "item_code", "item_value"]
    list_filter = ["catalog_version_id__catalog_id__code"]


admin.site.register(CatalogItem, CatalogItemAdmin)
