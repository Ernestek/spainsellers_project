from django.db import models


class BaseItem(models.Model):
    sku = models.CharField(max_length=256, unique=True)
    link = models.CharField(max_length=512)
    item_name = models.CharField(max_length=512)
    price = models.CharField(max_length=256)
    in_stock = models.BooleanField()
