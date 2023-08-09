import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import RepuestosfuentesLinks


class RepuestosfuentesLinksParser:
    BASE_URL = 'https://www.repuestosfuentes.es/'
    email = ''
    passwd = ''

    def __init__(self):
        browser_options = ChromeOptions()
        service_args = [
            '--start-maximized',

            # '--headless=True'
            # 
            # '--no-sandbox',
            # '--disable-web-security',
            # '--allow-running-insecure-content',
            # '--hide-scrollbars',
            # '--disable-setuid-sandbox',
            # '--profile-directory=Default',
            '--ignore-ssl-errors=true',
            # '--disable-dev-shm-usage'
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
        self.open_site(self.BASE_URL)

    def open_site(self, link):
        self.driver.get(link)
        self._wait_and_choose_element('#soy_menu_icon').click()

        # self._wait_and_choose_element('.soy_item_raiz').click()

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        list_categories = soup.select('.category-sub-menu a')
        for category in list_categories:
            url = category['href']
            self.driver.get(url)
            try:
                self._wait_and_choose_element('#soy_subcategories_block li a')
            except TimeoutException:
                RepuestosfuentesLinks.objects.get_or_create(
                    link=url
                )
                continue

            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            links = soup.select('#soy_subcategories_block li a')
            # links = self.driver.find_elements('#soy_subcategories_block li a')
            for link in links:
                RepuestosfuentesLinks.objects.get_or_create(
                    link=link['href']
                )

    def login(self):
        self.driver.get('https://www.repuestosfuentes.es/autenticacion?back=my-account')
        login = self._wait_and_choose_element('[id="login-form"] [name="email"]')
        login.clear()
        login.send_keys(self.email)
        passwd = self._wait_and_choose_element('[name="password"]')
        passwd.clear()
        passwd.send_keys(self.passwd)
        self._wait_and_choose_element('[id="submit-login"]').click()
        time.sleep(2)

    def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> WebElement:
        condition = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(self.driver, timeout).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


if __name__ == '__main__':
    with RepuestosfuentesLinksParser() as placer:
        placer.placer_repuestosfuentes_parser()
