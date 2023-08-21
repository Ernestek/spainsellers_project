import time

from selenium.common import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import PreciosadictosLinks, PreciosadictosItem


class PreciosadictosParser:
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

    def placer_preciosadictos_parser(self):
        self.login()
        self.get_all_items()

    def login(self):
        self.driver.get('https://www.preciosadictos.com/')
        try:
            self._wait_and_choose_element('[class="cookie-consent__popup-button"]').click()
        except TimeoutException:
            ...
        self._wait_and_choose_element('[class="lgin drpd tt tt-27 mhide"]').click()
        time.sleep(2)
        login = self._wait_and_choose_element('[name="email_address"]')
        login.clear()
        login.send_keys(self.email)
        passwd = self._wait_and_choose_element('[name="password"]')
        passwd.clear()
        passwd.send_keys(self.passwd)
        self._wait_and_choose_element('[class="rdbt mt-auto"]').click()
        time.sleep(2)

    def get_all_items(self):
        links = PreciosadictosLinks.objects.filter(status=False)
        for link in links:
            self.driver.get(link.link)
            try:
                self._wait_and_choose_element('[class="ax row prdt-grop prdt-grop-top"]', timeout=10)
            except TimeoutException:
                link.status = True
                link.save()
                continue
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
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

    def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> WebElement:
        condition = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(self.driver, timeout).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


if __name__ == '__main__':
    with PreciosadictosParser() as placer:
        placer.placer_preciosadictos_parser()
