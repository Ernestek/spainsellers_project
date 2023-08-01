import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from load_django import *
from parser_app.models import LcphonesLinks, LcphonesItem


class LcphonesParser:
    BASE_URL = 'https://lcphones.com/'

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
            '--disable-dev-shm-usage',
            '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
            'like Gecko) CriOS/86.0.4240.77 Mobile/15E148 Safari/604.1',

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
        browser_options.add_experimental_option("mobileEmulation", {
            "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
        })

        self.driver = Chrome(options=browser_options)

    def placer_lcphones_parser(self):
        self.open_site(self.BASE_URL)
        links = LcphonesLinks.objects.filter(status=False)
        for link in links:
            self.get_info_all_page(link)

    def open_site(self, link):
        self.driver.get(link)
        self._wait_and_choose_element('#top-links .dropdown-toggle').click()
        self._wait_and_choose_element('.dropdown-menu.dropdown-menu-right li:nth-of-type(2)').click()

        login = self._wait_and_choose_element('#input-email')
        login.clear()
        login.send_keys('iernestek@gmail.com')
        password = self._wait_and_choose_element('#input-password')
        password.clear()
        password.send_keys('ernestek2')
        self._wait_and_choose_element('.form-group + [class="btn btn-primary"]').click()
        self._wait_and_choose_element('.menu-mobile .navbar-toggle')

    def get_info_all_page(self, link):
        self.driver.get(link.link)
        while True:
            self.get_info_single_page()
            try:
                self._wait_and_choose_element(
                    '//a[text()=">"]', By.XPATH
                ).click()
            except TimeoutException:
                break
            time.sleep(3)
        link.status = True
        link.save()

    def get_info_single_page(self):
        time.sleep(5)
        self._wait_and_choose_element('.custom-category div.product-layout')
        items = self.driver.find_elements(
            By.CSS_SELECTOR,
            '.custom-category div.product-layout'
        )
        for item in items:
            try:
                link = item.find_element(
                    By.CSS_SELECTOR,
                    '.name a'
                ).get_attribute('href')
            except NoSuchElementException:
                link = None
            try:
                sku = link.split('product_id=')[-1]
            except NoSuchElementException:
                sku = None
            try:
                item_name = item.find_element(
                    By.CSS_SELECTOR,
                    '.name a'
                ).text.replace('\n', ' ').strip()
            except NoSuchElementException:
                item_name = None
            try:
                price = item.find_element(
                    By.CSS_SELECTOR,
                    '.price'
                ).text.split(':')[-1].replace('€', '').strip()
            except NoSuchElementException:
                price = None
            try:
                in_stock = item.find_element(
                    By.CSS_SELECTOR,
                    '.stock-status span'
                ).text.strip()
                in_stock = True if in_stock == 'Em stock' else False
            except NoSuchElementException:
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

    def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> WebElement:
        condition = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(self.driver, timeout).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


if __name__ == '__main__':
    with LcphonesParser() as placer:
        placer.placer_lcphones_parser()
