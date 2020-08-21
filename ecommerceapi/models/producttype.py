"""
    Product Type Model
    exports class:ProductType
    generated by: Bryan Nilsen
"""
from django.db import models


class ProductType(models.Model):
    """
    Stores the properties of a single product type.
    """

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("product_type")
        verbose_name_plural = ("product_types")

    def __str__(self):
        return self.name