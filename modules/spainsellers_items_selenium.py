import time

from selenium.common import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import SpainSellersItem, SpainSellersLinks


class SpainsellersParser:
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

    def placer_spainsellers_parser(self):
        self.login()
        self.get_all_items()

    def login(self):
        self.driver.get('https://www.spainsellers.com/inicio-sesion?back=my-account')
        login = self._wait_and_choose_element('input#email')
        login.clear()
        login.send_keys(self.email)
        passwd = self._wait_and_choose_element('input#passwd')
        passwd.clear()
        passwd.send_keys(self.passwd)
        self._wait_and_choose_element('[id="SubmitLogin"]').click()
        time.sleep(2)

    def get_all_items(self):
        links = SpainSellersLinks.objects.filter(status=False)
        for link in links:
            self.driver.get(link.link)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            self.get_info(soup)
            try:
                last_p = soup.select('.pagination li a')[-2].text
                for p in range(2, int(last_p) + 1):
                    self.driver.get(link.link + f'?p={p}')
                    time.sleep(1)
                    try:
                        self._wait_and_choose_element('[class="product_list grid row"]')
                    except TimeoutException:
                        continue
                    soup = BeautifulSoup(self.driver.page_source, 'lxml')
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

    def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> WebElement:
        condition = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(self.driver, timeout).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


if __name__ == '__main__':
    with SpainsellersParser() as placer:
        placer.placer_spainsellers_parser()
