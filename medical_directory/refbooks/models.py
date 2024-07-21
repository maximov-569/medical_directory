from django.db import models
from django.utils import timezone


class Catalog(models.Model):
    code = models.CharField(blank=False, unique=True, max_length=100)
    name = models.CharField(max_length=300, blank=False)
    description = models.TextField()


class CatalogVersion(models.Model):
    catalog_id = models.ForeignKey(Catalog, on_delete=models.CASCADE, blank=False)
    version = models.CharField(max_length=50, blank=False)
    version_start_date = models.DateField(blank=False, default=timezone.now().date())

    class Meta:
        unique_together = ("version", "catalog_id")
        constraints = [
            models.UniqueConstraint(
                fields=["catalog_id", "version_start_date"],
                name="unique_start_date_per_catalog",
            )
        ]


class CatalogItem(models.Model):
    catalog_version_id = models.ForeignKey(
        CatalogVersion, on_delete=models.CASCADE, blank=False
    )
    item_code = models.CharField(max_length=100, blank=False)
    item_value = models.CharField(max_length=300, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["catalog_version_id", "item_code"],
                name="unique_item_code_value_per_catalog_version",
            )
        ]
