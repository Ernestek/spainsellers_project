import requests
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import ChipspainLinks, ChipspainItem


class RepuestosfuentesParser:
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    def get_all_items(self):
        links = ChipspainLinks.objects.filter(status=False)
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
        items = soup.select('#product_list li')
        for item in items:
            try:
                link = item.select_one('h3 a')['href']
            except AttributeError:
                link = None
            try:
                sku = item.select_one('.exclusive.ajax_add_to_cart_button')['data-id-product'].split('_')[-1]
            except AttributeError:
                sku = None
            try:
                item_name = item.select_one('h3 a')['title']
            except AttributeError:
                item_name = None
            try:
                price = item.select_one('.price').text.replace('€', '').strip()
            except AttributeError:
                price = None
            try:
                in_stock = item.select_one('.available').text
                in_stock = True if in_stock == 'Disponible' else False
            except AttributeError:
                in_stock = False
            ChipspainItem.objects.get_or_create(
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









































