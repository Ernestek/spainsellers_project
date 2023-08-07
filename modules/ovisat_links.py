import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from load_django import *
from parser_app.models import OvisatLinks


class OvisatLinksParser:
    BASE_URL = 'https://www.ovisat.com/es'

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

    def placer_ovisat_parser(self):
        self.open_site(self.BASE_URL)

    def open_site(self, link):
        self.driver.get(link)
        time.sleep(3)
        self._wait_and_choose_element('[class="open_categories_sticky"]').click()
        categories = self.driver.find_elements(
            By.CSS_SELECTOR,
            '[class="theme_menu cats dropdown active visible"] [class="list_of_links"] li a'
        )
        list_categories = map(lambda x: x.get_attribute('href'), categories)
        for link in list_categories:
            print(link)
            OvisatLinks.objects.get_or_create(
                link=link
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
    with OvisatLinksParser() as placer:
        placer.placer_ovisat_parser()

