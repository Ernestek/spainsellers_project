import time

from selenium.common import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import FourPhonesLinks, FourPhonesItem


class FourPhonesLinksParser:
    BASE_URL = 'https://4phones.eu/'

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

    def placer_4phones_parser(self):
        self.open_site(self.BASE_URL)
        self.get_all_info()

    def open_site(self, link):
        self.driver.get(link)
        try:
            self._wait_and_choose_element('button.recommendation-modal__button', timeout=3).click()
        except TimeoutException:
            pass
        login = self._wait_and_choose_element('[id="customer[email]"]')
        login.clear()
        login.send_keys('email')  # send email
        password = self._wait_and_choose_element('[id="customer[password]"]')
        password.clear()
        password.send_keys('password')  # send password
        self._wait_and_choose_element('.action-login-primary').click()

    def get_all_info(self):
        links = FourPhonesLinks.objects.filter(status=False)
        for link in links:
            self.driver.get(link)

            self.get_info_per_page()
            pages = self.driver.find_elements(
                By.CSS_SELECTOR,
                '#pagination .page a'
            )[-1].text
            for page in range(2, int(pages) + 1):
                self.driver.get(link + f'?page={page}')
                time.sleep(1)
                self.get_info_per_page()
            link.status = True
            link.save()

    def get_info_per_page(self):
        try:
            self._wait_and_choose_element('[class="product-sku"]', timeout=7)
        except TimeoutException:
            return
        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        items = soup.select('.product-item')
        for item in items:
            try:
                link = 'https://4phones.eu' + item.select_one('a')['href']
            except AttributeError:
                link = None
            try:
                sku = item.select_one('[class="product-sku"]').text.replace('SKU:', '').strip()
            except AttributeError:
                sku = None
            try:
                item_name = item.select_one('[class="product-item__info-inner"] a').text
            except AttributeError:
                item_name = None
            try:
                price = item.select_one('.price').text.replace('€', '').strip()
            except AttributeError:
                price = None
            try:
                out_stock = item.select_one('[data-product-stock="0"]')
                in_stock = False if out_stock else True
            except AttributeError:
                in_stock = True
            FourPhonesItem.objects.get_or_create(
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
    with FourPhonesLinksParser() as placer:
        placer.placer_4phones_parser()
