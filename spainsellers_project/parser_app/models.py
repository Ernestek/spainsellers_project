from django.db import models


class SpainSellersItem(models.Model):
    sku = models.CharField(max_length=256, unique=True)
    link = models.CharField(max_length=512)
    item_name = models.CharField(max_length=512)
    price = models.CharField(max_length=256, null=True, blank=True)
    in_stock = models.BooleanField()

    class Meta:
        verbose_name = 'SpainSellersItem'
        verbose_name_plural = 'SpainSellersItems'


class RepuestosfuentesLinks(models.Model):
    link = models.CharField(max_length=512, unique=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'RepuestosfuentesLink'
        verbose_name_plural = 'RepuestosfuentesLinks'


class RepuestosfuentesItem(models.Model):
    sku = models.CharField(max_length=256, unique=True)
    link = models.CharField(max_length=512)
    item_name = models.CharField(max_length=512)
    price = models.CharField(max_length=256, null=True, blank=True)
    in_stock = models.BooleanField()

    class Meta:
        verbose_name = 'RepuestosfuentesItem'
        verbose_name_plural = 'RepuestosfuentesItems'


class PreciosadictosLinks(models.Model):
    link = models.CharField(max_length=512, unique=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'PreciosadictosLink'
        verbose_name_plural = 'PreciosadictosLinks'


class PreciosadictosItem(models.Model):
    sku = models.CharField(max_length=256, unique=True)
    link = models.CharField(max_length=512)
    item_name = models.CharField(max_length=512)
    price = models.CharField(max_length=256, null=True, blank=True)
    in_stock = models.BooleanField()

    class Meta:
        verbose_name = 'PreciosadictosItem'
        verbose_name_plural = 'PreciosadictosItems'


class ChipspainLinks(models.Model):
    link = models.CharField(max_length=512, unique=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ChipspainLink'
        verbose_name_plural = 'ChipspainLinks'


class ChipspainItem(models.Model):
    sku = models.CharField(max_length=256, unique=True)
    link = models.CharField(max_length=512)
    item_name = models.CharField(max_length=512)
    price = models.CharField(max_length=256, null=True, blank=True)
    in_stock = models.BooleanField()

    class Meta:
        verbose_name = 'ChipspainItem'
        verbose_name_plural = 'ChipspainItems'


class LcphonesLinks(models.Model):
    link = models.CharField(max_length=512, unique=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'LcphonesLink'
        verbose_name_plural = 'LcphonesLinks'


class LcphonesItem(models.Model):
    sku = models.CharField(max_length=256, unique=True)
    link = models.CharField(max_length=512)
    item_name = models.CharField(max_length=512)
    price = models.CharField(max_length=256, null=True, blank=True)
    in_stock = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = 'LcphonesItem'
        verbose_name_plural = 'LcphonesItems'


class OvisatLinks(models.Model):
    link = models.CharField(max_length=512, unique=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'OvisatLink'
        verbose_name_plural = 'OvisatLinks'


class OvisatItem(models.Model):
    sku = models.CharField(max_length=256, unique=True)
    link = models.CharField(max_length=512)
    item_name = models.CharField(max_length=512)
    price = models.CharField(max_length=256, null=True, blank=True)
    in_stock = models.BooleanField()

    class Meta:
        verbose_name = 'OvisatItem'
        verbose_name_plural = 'OvisatItems'
