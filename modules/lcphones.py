import requests
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import LcphonesLinks, LcphonesItem


class LcphonesParser:
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
    }

    def get_all_items(self):
        links = LcphonesLinks.objects.filter(status=False)
        for link in links:
            page = self.session.get(url=link.link, headers=self.headers).content
            soup = BeautifulSoup(page, 'lxml')
            self.get_info_per_page(soup)

            pages = soup.select('.sortPagiBar .pagination li a')[-2].text
            for page in range(2, int(pages) + 1):
                page = self.session.get(url=link.link, params={'p': page}, headers=self.headers).content
                soup = BeautifulSoup(page, 'lxml')
                self.get_info_per_page(soup)

            link.status = True
            link.save()

    def get_info_per_page(self, soup: BeautifulSoup):
        items = soup.select('.custom-products div.product-layout')
        for item in items:
            try:
                link = item.select_one('.name a')['href']
            except AttributeError:
                link = None
            try:
                sku = item.select_one('[name="product_id"]')['value']
            except AttributeError:
                sku = None
            try:
                item_name = item.select_one('.description').text.strip()
            except AttributeError:
                item_name = None
            try:
                price = item.select_one('.price').text.replace('€', '').strip()
            except AttributeError:
                price = None
            try:
                in_stock = item.select_one('.stock-status span').text
                in_stock = True if in_stock == 'Em stock' else False
            except AttributeError:
                in_stock = None

            LcphonesItem.objects.get_or_create(
                sku=sku,
                defaults={
                    'link': link,
                    'item_name': item_name,
                    'price': price,
                    'in_stock': in_stock,
                },
            )


if __name__ == '__main__':
    LcphonesParser().get_all_items()









































