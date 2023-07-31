from django.contrib import admin

from parser_app.models import SpainSellersItem, RepuestosfuentesItem, PreciosadictosItem

base_display = ('sku', 'item_name', 'price', 'link', 'in_stock')


@admin.register(SpainSellersItem)
class SpainSellersItemAdmin(admin.ModelAdmin):
    list_display = base_display


@admin.register(RepuestosfuentesItem)
class RepuestosfuentesItemAdmin(admin.ModelAdmin):
    list_display = base_display


@admin.register(PreciosadictosItem)
class PreciosadictosItemAdmin(admin.ModelAdmin):
    list_display = base_display
