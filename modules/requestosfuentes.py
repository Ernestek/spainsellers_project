import requests
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import RepuestosfuentesItem, RepuestosfuentesLinks


class RepuestosfuentesParser:
    BASE_URL = 'https://www.spainsellers.com/servicio-tecnico/'
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    def get_all_links(self):
        links = RepuestosfuentesLinks.objects.filter(status=False)
        for link in links:
            page = requests.get(link.link, headers=self.headers)
            soup = BeautifulSoup(page.content, 'lxml')
            for item in soup.select('#soy_subcategories_block li a'):
                RepuestosfuentesLinks.objects.get_or_create(link=item['href'])

    def get_all_items(self):
        links = RepuestosfuentesLinks.objects.filter(status=False)
        for link in links:
            page = self.session.get(url=link.link, headers=self.headers).content
            soup = BeautifulSoup(page, 'lxml')
            self.get_info(soup)
            link.status = True
            link.save()

    def get_info(self, soup: BeautifulSoup):
        items = soup.select('#js-product-list  .product-miniature')
        for item in items:
            try:
                link = item.select_one('a')['href']
            except AttributeError:
                link = None
            try:
                sku = item['data-id-product']
            except AttributeError:
                sku = None
            try:
                item_name = item.select_one('.product-title').text
            except AttributeError:
                item_name = None
            try:
                price = item.select_one('.price').text.replace('€', '').strip()
            except AttributeError:
                price = None
            try:
                in_stock = item.select_one('.hidden-lg-up').text
                in_stock = True if in_stock == 'Comprar' else False
            except AttributeError:
                in_stock = False
            else:
                in_stock = True if in_stock else False
            RepuestosfuentesItem.objects.get_or_create(
                sku=sku,
                defaults={
                    'link': link,
                    'item_name': item_name,
                    'price': price,
                    'in_stock': in_stock,
                },
            )


if __name__ == '__main__':
    RepuestosfuentesParser().get_all_items()









































