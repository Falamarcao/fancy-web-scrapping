import traceback
from time import sleep
from random import randrange

from selenium.webdriver import Remote
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# from selenium.common.exceptions import TimeoutException

from .navigator.navigation_guide import NavigationGuide


class ChromeDriver:

    def __init__(self, url: str, navigation: NavigationGuide):
        self.url: str = url
        self.navigation_guide: NavigationGuide = navigation
        self.driver: Remote = Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

    def __quit_on_error(self, method) -> None:
        try:
            method()
        except Exception as e:
            print("\n\n", "-"*10, "\n", str(e), "\n",
                  traceback.format_exc(), "-"*10, "\n\n")
            self.driver.quit()

    @staticmethod
    def wait(start: int = 3, stop: int = 6) -> int:
        return randrange(start, stop, 1)

    def start(self) -> None:
        def _():
            self.driver.get(self.url)

            actions = ActionChains(self.driver)
            actions.pause(self.wait())

            for navigation_command in self.navigation_guide:
                print(navigation_command.to_dict())

                # Wait for element presence
                WebDriverWait(self.driver, self.wait()).until(
                    EC.presence_of_element_located((navigation_command.by, navigation_command.path)))

                # Find element by XPATH
                element = self.driver.find_element(
                    navigation_command.by, navigation_command.path)

                # Schedule actions
                for action in navigation_command.actions:
                    getattr(actions, action)(element)
                    # Schedule pause action of [t] seconds
                    actions.pause(self.wait())

            # Perform actions from the ActionChain
            actions.perform()

        # Execute method and onError QUIT Selenium's session.
        self.__quit_on_error(_)

    def quit(self, sleep_seconds: int = 0) -> None:
        sleep(sleep_seconds)
        self.driver.quit()
