import requests
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import PreciosadictosLinks, PreciosadictosItem


class RepuestosfuentesParser:
    BASE_URL = 'https://www.preciosadictos.com/'
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    def get_all_links(self):
        links = PreciosadictosLinks.objects.filter(status=False)
        for link in links:
            page = requests.get(link.link, headers=self.headers)
            soup = BeautifulSoup(page.content, 'lxml')
            for item in soup.select('#categories a'):
                PreciosadictosLinks.objects.get_or_create(link=item['href'])

    def get_all_items(self):
        links = PreciosadictosLinks.objects.filter(status=False)
        for link in links:
            page = self.session.get(url=link.link, headers=self.headers).content
            soup = BeautifulSoup(page, 'lxml')
            self.get_info(soup)
            link.status = True
            link.save()

    def get_info(self, soup: BeautifulSoup):
        items = soup.select('[class="ax row prdt-grop prdt-grop-top"] .prdt.col.a03.t04.m06.xprdt')
        for item in items:
            try:
                link = item.select_one('a.titu')['href']
            except AttributeError:
                link = None
            try:
                sku = item.select_one('a')['data-pid']
            except AttributeError:
                sku = None
            try:
                item_name = item.select_one('a.titu')['title']
            except AttributeError:
                item_name = None
            try:
                price = item.select_one('.prco').text.replace('€', '').strip()
            except AttributeError:
                price = None
            try:
                in_stock = item.select_one('.stock').text
                in_stock = True if in_stock == 'En STOCK' else False
            except AttributeError:
                in_stock = False
            print({
                    'link': link,
                    'item_name': item_name,
                    'price': price,
                    'in_stock': in_stock,
                })
            PreciosadictosItem.objects.get_or_create(
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









































