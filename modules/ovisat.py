import requests
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import OvisatLinks, OvisatItem


class OvisatParser:
    BASE_URL = 'https://www.preciosadictos.com/'
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    def get_all_links(self):
        links = OvisatLinks.objects.filter(status=False)
        for link in links:
            page = requests.get(link.link, headers=self.headers)
            soup = BeautifulSoup(page.content, 'lxml')
            for item in soup.select('#categories a'):
                OvisatLinks.objects.get_or_create(link=item['href'])

    def get_all_items(self):
        links = OvisatLinks.objects.filter(status=False)
        for link in links:
            page = self.session.get(url=link.link, headers=self.headers).content
            soup = BeautifulSoup(page, 'lxml')
            self.get_info(soup)
            try:
                pages = soup.select('.paginacion a')[-2].text
                for page in range(2, int(pages) + 1):
                    page = self.session.get(url=link.link, params={'pag': page}, headers=self.headers).content
                    soup = BeautifulSoup(page, 'lxml')
                    self.get_info(soup)
            except IndexError:
                pass
            link.status = True
            link.save()

    def get_info(self, soup: BeautifulSoup):
        items = soup.select('.productos-list .product_item')
        for item in items:
            try:
                link = item.select_one('.description a')['href']
            except AttributeError:
                link = None
            try:
                sku = link.split('-p')[-1]
            except AttributeError:
                sku = None
            try:
                item_name = item.select_one('.description a').text
            except AttributeError:
                item_name = None
            try:
                price = item.select_one('.description .pvp').text.replace('€', '').strip()
            except AttributeError:
                price = None
            try:
                in_stock = item.select_one('[class="tooltip_container stock stock-si"]')
                in_stock = True if in_stock else False
            except AttributeError:
                in_stock = False

            OvisatItem.objects.get_or_create(
                sku=sku,
                defaults={
                    'link': link,
                    'item_name': item_name,
                    'price': price,
                    'in_stock': in_stock,
                },
            )


if __name__ == '__main__':
    OvisatParser().get_all_links()
    OvisatParser().get_all_items()










































