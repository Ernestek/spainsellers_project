from django.http import JsonResponse

from parser_app.models import (
    OvisatItem,
    LcphonesItem,
    ChipspainItem,
    FourPhonesItem,
    RepuestosfuentesItem,
    PreciosadictosItem,
    SpainSellersItem,
)


def json_request(request, db):
    items = db.objects.all()
    items = [{
        'sku': item.sku,
        'link': item.link,
        'item_name': item.item_name,
        'price': item.price,
        'in_stock': item.in_stock,
    } for item in items]
    return JsonResponse(items, safe=False)


def ovisat(request):
    items = OvisatItem.objects.all()
    items = [{
        'sku': item.sku,
        'link': item.link,
        'item_name': item.item_name,
        'price': item.price,
        'in_stock': item.in_stock,
    } for item in items]
    return JsonResponse(items, safe=False)


def lcphones(request):
    items = LcphonesItem.objects.all()
    items = [{
        'sku': item.sku,
        'link': item.link,
        'item_name': item.item_name,
        'price': item.price,
        'in_stock': item.in_stock,
    } for item in items]
    return JsonResponse(items, safe=False)


def chipspain(request):
    items = ChipspainItem.objects.all()
    items = [{
        'sku': item.sku,
        'link': item.link,
        'item_name': item.item_name,
        'price': item.price,
        'in_stock': item.in_stock,
    } for item in items]
    return JsonResponse(items, safe=False)


def fourphones(request):
    items = FourPhonesItem.objects.all()
    items = [{
        'sku': item.sku,
        'link': item.link,
        'item_name': item.item_name,
        'price': item.price,
        'in_stock': item.in_stock,
    } for item in items]
    return JsonResponse(items, safe=False)


def repuestosfuentes(request):
    items = RepuestosfuentesItem.objects.all()
    items = [{
        'sku': item.sku,
        'link': item.link,
        'item_name': item.item_name,
        'price': item.price,
        'in_stock': item.in_stock,
    } for item in items]
    return JsonResponse(items, safe=False)


def preciosadictos(request):
    items = PreciosadictosItem.objects.all()
    items = [{
        'sku': item.sku,
        'link': item.link,
        'item_name': item.item_name,
        'price': item.price,
        'in_stock': item.in_stock,
    } for item in items]
    return JsonResponse(items, safe=False)


def spainsellers(request):
    items = SpainSellersItem.objects.all()
    items = [{
        'sku': item.sku,
        'link': item.link,
        'item_name': item.item_name,
        'price': item.price,
        'in_stock': item.in_stock,
    } for item in items]
    return JsonResponse(items, safe=False)
