# from selenium.common import TimeoutException, NoSuchElementException
# from selenium.webdriver import Chrome, ChromeOptions
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webelement import WebElement
#
# from load_django import *
# from parser_app.models import Info, Keywords
#
#
# class CosdnaParser:
#     BASE_URL = 'https://cosdna.com/eng/ingredients.php'
#
#     def __init__(self):
#         browser_options = ChromeOptions()
#         service_args = [
#             '--start-maximized',
#             '--no-sandbox',
#             '--disable-web-security',
#             '--allow-running-insecure-content',
#             '--hide-scrollbars',
#             '--disable-setuid-sandbox',
#             '--profile-directory=Default',
#             '--ignore-ssl-errors=true',
#             '--disable-dev-shm-usage'
#         ]
#         for arg in service_args:
#             browser_options.add_argument(arg)
#
#         browser_options.add_experimental_option(
#             'excludeSwitches', ['enable-automation']
#         )
#         browser_options.add_experimental_option('prefs', {
#             'profile.default_content_setting_values.notifications': 2,
#             'profile.default_content_settings.popups': 0
#         })
#
#         self.driver = Chrome(options=browser_options)
#
#     def placer_cosdna_parser(self):
#         keywords = Keywords.objects.filter(status='New')
#         for keyword in keywords:
#             try:
#                 self.open_site(keyword)
#                 self.get_info(keyword)
#             except TimeoutException:
#                 continue
#
#     def open_site(self, keyword):
#         self.driver.get(self.BASE_URL)
#         elem = self._wait_and_choose_element('[class="form-control mb-3"]')
#         elem.clear()
#         elem.send_keys(keyword.name)
#         self._wait_and_choose_element('[class="btn btn-primary"]').click()
#
#     def get_info(self, keyword):
#         self._wait_and_choose_element('[class="table table-hover border border-secondary"]')
#         try:
#             self._wait_and_choose_element('td [class="text-muted"]', timeout=1)
#         except TimeoutException:
#             pass
#         else:
#             keyword.status = 'No result'
#             keyword.save()
#             return
#
#         try:
#             result_keyword = self.driver.find_element(
#                 By.CSS_SELECTOR,
#                 '[class="tr-i"] td:nth-of-type(1)'
#             ).text.strip()
#         except NoSuchElementException:
#             result_keyword = None
#         try:
#             acne = self.driver.find_element(
#                 By.CSS_SELECTOR,
#                 '[class="tr-i"] td:nth-of-type(3)'
#             ).text.strip()
#         except NoSuchElementException:
#             acne = None
#         try:
#             irriant = self.driver.find_element(
#                 By.CSS_SELECTOR,
#                 '[class="tr-i"] td:nth-of-type(4)'
#             ).text.strip()
#         except NoSuchElementException:
#             irriant = None
#         try:
#             safety = self.driver.find_element(
#                 By.CSS_SELECTOR,
#                 '[class="tr-i"] td:nth-of-type(5)'
#             ).text.strip()
#         except NoSuchElementException:
#             safety = None
#         self._wait_and_choose_element('td > a').click()
#         self._wait_and_choose_element('[class="mb-2"]')
#         try:
#             synonyms = self.driver.find_element(
#                 By.CSS_SELECTOR,
#                 '[class="mb-2"]'
#             ).text.strip()
#         except NoSuchElementException:
#             synonyms = None
#         try:
#             description = self.driver.find_element(
#                 By.CSS_SELECTOR,
#                 '[class="linkb1 ls-2 lh-155"]'
#             ).text.replace('\n', ' ').strip()
#         except NoSuchElementException:
#             description = None
#         defaults = {
#             # 'searched_keyword': keyword,
#             'result_keyword': result_keyword,
#             'acne': acne,
#             'irriant': irriant,
#             'synonyms': synonyms,
#             'description': description,
#             'safety': safety,
#         }
#         print(defaults)
#         Info.objects.get_or_create(
#             searched_keyword=keyword.name,
#             defaults=defaults
#         )
#         keyword.status = 'Old'
#         keyword.save()
#
#     def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> WebElement:
#         condition = EC.presence_of_element_located((by, selector))
#         element = WebDriverWait(self.driver, timeout).until(condition)
#         return element
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.driver.close()
#
#
# if __name__ == '__main__':
#     with CosdnaParser() as placer:
#         placer.placer_cosdna_parser()
