from time import sleep

from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ChromeDriver:

    def __init__(self, url: str, xpath_list: list[str]):
        self.url: str = url
        self.xpath_list: list[str] = xpath_list
        self.driver: webdriver.Remote = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

    def _quit_on_error(self, method):
        try:
            method()
        except:
            self.quit()

    def start(self):
        def _():
            self.driver.get(self.url)

            for xpath in self.xpath_list:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))

        self._quit_on_error(_)

    def quit(self, sleep_seconds: int = 0):
        sleep(sleep_seconds)
        self.driver.quit()
