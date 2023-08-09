from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import ChipspainLinks


class ChipspainLinksParser:
    BASE_URL = 'https://www.chipspain.com/es/'
    email = ''
    passwd = ''

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

    def placer_chipspain_parser(self):
        self.login()
        self.open_site(self.BASE_URL)

    def open_site(self, link):
        self.driver.get(link)
        self._wait_and_choose_element('[id="chiptopmenu_showmenu"] span')

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        list_categories = soup.select('[id="chiptopmenu_ul"] ul li a')
        print(len(list_categories))
        for item in list_categories:
            ChipspainLinks.objects.get_or_create(
                link=item['href']
            )

    def login(self):
        self.driver.get('https://www.chipspain.com/es/inicio-sesion?back=my-account')
        login = self._wait_and_choose_element('input#email')
        login.clear()
        login.send_keys(self.email)
        password = self._wait_and_choose_element('input#passwd')
        password.clear()
        password.send_keys(self.passwd)
        self._wait_and_choose_element('input#SubmitLogin').click()

    def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> WebElement:
        condition = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(self.driver, timeout).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


if __name__ == '__main__':
    with ChipspainLinksParser() as placer:
        placer.placer_chipspain_parser()
