import time

from bs4 import BeautifulSoup
from selenium.common import TimeoutException
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
        self.login()
        self.open_site(self.BASE_URL)

    def open_site(self, link):
        # self.driver.get(link)
        # time.sleep(3)
        # try:
        #     self._wait_and_choose_element('[class="fancybox-item fancybox-close"]').click()
        # except TimeoutException:
        #     pass
        # time.sleep(1)
        # try:
        #     self._wait_and_choose_element('[class="open_categories_sticky"]').click()
        # except TimeoutException:
        #     pass

        # categories = self.driver.find_elements(
        #     By.CSS_SELECTOR,
        #     '[class="theme_menu cats dropdown active visible"] [class="list_of_links"] li a'
        # )
        time.sleep(3)

        # list_categories = map(lambda x: x.get_attribute('href'), categories)
        categories = [
            'https://www.ovisat.com/es/tienda-telefonia-movil-t1',
            'https://www.ovisat.com/es/tienda-electronica-t4',
            'https://www.ovisat.com/es/tienda-llaves-y-mandos-t3',
            'https://www.ovisat.com/es/tienda-automovil-pantallas-coche-t16',
            'https://www.ovisat.com/es/tienda-consolas-t2',
            'https://www.ovisat.com/es/tienda-informatica-t9',
            'https://www.ovisat.com/es/tienda-impresion3d-t13',
            'https://www.ovisat.com/es/tienda-baterias-t10',
            'https://www.ovisat.com/es/tienda-herramientas-t14',
            'https://www.ovisat.com/es/tienda-patinetes-t15',
        ]
        for link in categories:
            self.driver.get(link)
            time.sleep(2)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            for item in soup.select('[class="theme_menu cats"] li a'):
                OvisatLinks.objects.get_or_create(link='https://www.ovisat.com' + item['href'])


    def login(self):
        self.driver.get('https://www.ovisat.com/es/login')
        time.sleep(3)
        try:
            self._wait_and_choose_element('[class="fancybox-item fancybox-close"]').click()
        except TimeoutException:
            pass
        login = self._wait_and_choose_element('[id="l_email"]')
        login.clear()
        login.send_keys('')
        passwd = self._wait_and_choose_element('[id="l_pass"]')
        passwd.clear()
        passwd.send_keys('')
        self._wait_and_choose_element('[id="botoneraform1"] button').click()

    # def get_all_links(self):
    #     # links = OvisatLinks.objects.filter(status=False)
    #     for link in links:
    #         # page = requests.get(link.link, headers=self.headers)
    #         soup = BeautifulSoup(self.driver.page_source, 'lxml')
    #         for item in soup.select('#categories a'):
    #             OvisatLinks.objects.get_or_create(link=item['href'])

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

