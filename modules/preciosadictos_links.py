import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import PreciosadictosLinks


class PreciosadictosLinksParser:
    BASE_URL = 'https://www.preciosadictos.com/'

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
        self.open_site(self.BASE_URL)

    def open_site(self, link):
        self.driver.get(link)
        try:
            self._wait_and_choose_element('[class="cookie-consent__popup-button"]').click()
        except TimeoutException:
            ...
        self._wait_and_choose_element('#main-fake').click()

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        list_categories = soup.select('[class="mm-arrow"] a')
        list_categories = map(lambda x: x['href'], list_categories)
        self.get_links(list_categories)

        self.driver.get(link)
        try:
            self._wait_and_choose_element('[class="cookie-consent__popup-button"]').click()
        except TimeoutException:
            ...
        self._wait_and_choose_element('#main-fake').click()
        parent_cat = self.driver.find_elements(
            By.CSS_SELECTOR,
            '[class="mm-arrow mm-child"] a'
        )
        parent_cat = list(map(lambda x: x.get_attribute('data-href'), parent_cat))
        for link in parent_cat:
            self.driver.get(link)
            try:
                self._wait_and_choose_element('#categories', timeout=5)
                self._wait_and_choose_element('[class="col a03 t04 m12"]', timeout=4)
            except TimeoutException:
                PreciosadictosLinks.objects.get_or_create(
                    link=link
                )
                continue
            links = self.driver.find_elements(
                By.CSS_SELECTOR,
                '[class="col a03 t04 m12"] a'
            )
            list_categories = list(map(lambda x: x.get_attribute('href'), links))
            self.get_links(list_categories)

    def get_links(self, list_categories):
        for category in list_categories:

            self.driver.get(category)
            try:
                self._wait_and_choose_element('#categories', timeout=2)
                self._wait_and_choose_element('[class="col a03 t04 m12"]', timeout=4)
                PreciosadictosLinks.objects.get_or_create(
                    link=category
                )
            except TimeoutException:
                continue
            links = self.driver.find_elements(
                By.CSS_SELECTOR,
                '[class="col a03 t04 m12"] a'
            )
            for link in links:
                print(link.get_attribute('href'))
                PreciosadictosLinks.objects.get_or_create(
                    link=link.get_attribute('href')
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
    with PreciosadictosLinksParser() as placer:
        placer.placer_preciosadictos_parser()
