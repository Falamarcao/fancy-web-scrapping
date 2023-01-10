import traceback
from time import sleep
from typing import Union
from random import randrange

from selenium.webdriver import Remote, ChromeOptions

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException

from .navigator.navigation_guide import NavigationGuide
from .navigator.navigation_command import NavigationCommand
from .humanizer.humanizer import Humanizer

from celery import current_app


class ChromeDriver:

    def __init__(self, url: str, navigation: NavigationGuide):
        self.url: str = url
        self.navigation_guide: NavigationGuide = navigation

        # Initializing Chrome Options from the Webdriver
        chrome_options = ChromeOptions()
        # Adding Argument to Not Use Automation Extension
        chrome_options.add_experimental_option("useAutomationExtension", False)
        # Excluding enable-automation Switch
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("disable-popup-blocking")
        chrome_options.add_argument("disable-notifications")
        chrome_options.add_argument("disable-gpu")  # renderer timeout

        self.driver: WebDriver = Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            options=chrome_options)
        self.human = Humanizer(driver=self.driver)
        self.actions: ActionChains = ActionChains(self.driver)
        self.data: dict = {}

    def __on_error(self, method) -> None:
        try:
            method()
        except Exception as e:
            print("\n\n", "-"*10, "\n", str(e), "\n",
                  traceback.format_exc(), "-"*10, "\n\n")

    @staticmethod
    def wait(start: int = 3, stop: int = 6) -> int:
        return randrange(start, stop, 1)

    def find_element_by(self, by, path, many: bool = False) -> Union[list[WebElement], WebElement]:
        try:
            # 1. Wait for element presence
            WebDriverWait(self.driver, self.wait()).until(
                EC.presence_of_element_located((by, path)))  # FIXME: Unable to determine element locating strategy

            # 2. Find element(s) by...
            if many:
                return self.driver.find_elements(by, path)
            return self.driver.find_element(by, path)
        except TimeoutException:
            raise Exception(f"Element {path} was not found by {by}")

    def actions_chain(self, navigation_command: NavigationCommand, elements: Union[list[WebElement], WebElement]):
        for action in navigation_command.actions:
            print(action, '%'*30)
            if action == 'create_entry':

                for _ in self.data:
                    for element in elements:
                        self.data.update(
                            {navigation_command.human_label: element.text})

            elif action == 'perform_create_entry':
                current_app.send_task(
                    'movie_listing.webscraper.tasks.create_entry',
                    model_name=navigation_command.model_name, data=self.data)

            elif action == 'move_to_element_with_offset':
                self.actions.move_by_offset(8, 0)
                self.actions.pause(self.wait())

                offset = self.human.wind_mouse(8, 0, elements)

                self.actions.move_to_element_with_offset(
                    elements, offset[0], offset[1])
                # Schedule pause action of [t] seconds
                self.actions.pause(self.wait())

            elif action == 'scroll_page':
                Humanizer.scroll_page(elements)

            elif action == 'perform_actions':
                # 4. Perform actions from the ActionChain
                self.actions.perform()

            else:
                getattr(self.actions, action)(elements)
                # Schedule pause action of [t] seconds
                self.actions.pause(self.wait())

    def start(self) -> None:
        def _():
            self.driver.get(self.url)

            self.actions.pause(self.wait())

            for navigation_command in self.navigation_guide:

                if navigation_command.subcommands:
                    for subcommand in navigation_command.subcommands:
                        element = self.find_element_by(
                            subcommand.by, subcommand.path, many=subcommand.many)

                    self.actions_chain(subcommand, element)
                else:
                    elements = self.find_element_by(navigation_command.by,
                                                    navigation_command.path)

                    self.actions_chain(navigation_command, elements)

        self.__on_error(_)

    def quit(self, sleep_seconds: int = 0) -> None:
        sleep(sleep_seconds)
        self.driver.quit()
