import requests
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import SpainSellersItem


class BrokersParser:
    BASE_URL = 'https://www.spainsellers.com/servicio-tecnico/'
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    def get_brokers(self):
        links = [
            'https://www.spainsellers.com/servicio-tecnico/',
            'https://www.spainsellers.com/repuestos-moviles/',
            'https://www.spainsellers.com/repuestos-tablets/',
            'https://www.spainsellers.com/relojes-deportivos-o-smartwhatch/',
            'https://www.spainsellers.com/repuestos-videoconsolas/',
            'https://www.spainsellers.com/informatica/',
            'https://www.spainsellers.com/repuestos-drone/',
            'https://www.spainsellers.com/repuestos-patinete-electrico/',
            'https://www.spainsellers.com/consumibles/',
        ]
        for link in links:
            page = self.session.get(url=link, headers=self.headers).content
            soup = BeautifulSoup(page, 'lxml')
            self.get_info(soup)
            try:
                last_p = soup.select('.pagination li a')[-2].text
                for p in range(2, int(last_p) + 1):
                    page = self.session.get(url=link, params={'p': p}, headers=self.headers).content
                    soup = BeautifulSoup(page, 'lxml')
                    self.get_info(soup)
            except IndexError:
                pass

    def get_info(self, soup: BeautifulSoup):
        items = soup.select('.product-container')
        for item in items:
            try:
                link = item.select_one('.product-name')['href']
            except AttributeError:
                link = None
            try:
                sku = item.select_one('.product-reference').text
            except AttributeError:
                sku = None
            try:
                item_name = item.select_one('.product-name')['title']
            except AttributeError:
                item_name = None
            try:
                price = item.select_one('.product-price').text.strip()[1:]
            except AttributeError:
                price = None
            try:
                in_stock = item.select_one('.button-container > div')
            except AttributeError:
                in_stock = False
            else:
                in_stock = True if in_stock else False

            SpainSellersItem.objects.get_or_create(
                sku=sku,
                defaults={
                    'link': link,
                    'item_name': item_name,
                    'price': price,
                    'in_stock': in_stock,
                },
            )


if __name__ == '__main__':
    BrokersParser().get_brokers()
