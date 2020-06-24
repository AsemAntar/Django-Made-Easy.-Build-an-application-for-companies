from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True, default="")
    short_code = models.CharField(max_length=20)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
