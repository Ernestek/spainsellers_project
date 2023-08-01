from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import LcphonesLinks


class LcphonesLinksParser:
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

    def open_site(self, link):
        self.driver.get(link)
        self._wait_and_choose_element('[class="btn btn-navbar navbar-toggle"]').click()

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        list_categories = soup.select('[id="ma-mobilemenu"] li a')
        for item in list_categories:
            LcphonesLinks.objects.get_or_create(
                link=item['href']
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
    with LcphonesLinksParser() as placer:
        placer.placer_lcphones_parser()
