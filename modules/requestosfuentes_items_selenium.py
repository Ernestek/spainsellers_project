import time

from selenium.common import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import RepuestosfuentesItem, RepuestosfuentesLinks


class RepuestosfuentesParser:
    email = 'geral@isell.pt'
    passwd = 'Oleg123!'

    def __init__(self):
        browser_options = ChromeOptions()
        service_args = [
            '--start-maximized',
            '--no-sandbox',
            '--disable-web-security',
            '--allow-running-insecure-content',
            '--hide-scrollbars',
            '--disable-setuid-sandbox',
            '--profile-directory=Default',
            '--ignore-ssl-errors=true',
            '--disable-dev-shm-usage'
        ]
        for arg in service_args:
            browser_options.add_argument(arg)

        browser_options.add_experimental_option(
            'excludeSwitches', ['enable-automation']
        )
        browser_options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0
        })

        self.driver = Chrome(options=browser_options)

    def placer_repuestosfuentes_parser(self):
        self.login()
        self.get_all_items()

    def login(self):
        self.driver.get('https://www.repuestosfuentes.es/autenticacion?back=my-account')
        login = self._wait_and_choose_element('[id="login-form"] [name="email"]')
        login.clear()
        login.send_keys(self.email)
        passwd = self._wait_and_choose_element('[name="password"]')
        passwd.clear()
        passwd.send_keys(self.passwd)
        elem = self._wait_and_choose_element('[id="submit-login"]')
        self.driver.execute_script(f"window.scrollBy(0, 200);")
        elem.click()
        time.sleep(2)

    def get_all_items(self):
        links = RepuestosfuentesLinks.objects.filter(status=False)
        for link in links:
            self.driver.get(link.link)
            try:
                self._wait_and_choose_element('[id="js-product-list"]', timeout=5)
            except TimeoutException:
                continue
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            self.get_info(soup)
            try:
                pages = soup.select('[class="page-list clearfix text-sm-center"] li a')[-2].text
            except (IndexError, AttributeError):
                link.status = True
                link.save()
                continue
            for page in range(2, int(pages) + 1):
                self.driver.get(link.link + f'?page={page}')
                time.sleep(1)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                self.get_info(soup)
            link.status = True
            link.save()

    def get_info(self, soup: BeautifulSoup):
        items = soup.select('#js-product-list .product-miniature')
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

    def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> WebElement:
        condition = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(self.driver, timeout).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


if __name__ == '__main__':
    with RepuestosfuentesParser() as placer:
        placer.placer_repuestosfuentes_parser()
