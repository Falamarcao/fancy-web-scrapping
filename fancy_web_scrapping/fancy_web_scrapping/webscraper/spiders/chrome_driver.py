import traceback
from time import sleep
from typing import Union, Callable
from random import randrange

from selenium.webdriver import Remote, ChromeOptions

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.common.keys import Keys
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
        self.data: list[dict] = []

    @staticmethod
    def __on_error(method: Callable) -> None:
        try:
            method()
        except Exception as e:
            print("\n\n", "-"*10, "\n", str(e), "\n",
                  traceback.format_exc(), "-"*10, "\n\n")

    def __param_is_required(action: str, method: Callable, param: str):
        if param != None and param != '':
            method()
        else:
            raise Exception(f"Action {action} requires a parameter")

    @staticmethod
    def batch(iterable):
        """
        Splits an iterable into multiple batches.    
        """
        l = len(iterable)
        n = round(l/2)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]

    @staticmethod
    def wait(start: int = 2, stop: int = 4) -> int:
        return randrange(start, stop, 1)

    def find_element_by(self, by, path, many: bool) -> Union[list[WebElement], WebElement]:
        try:
            # 1. Wait for element presence
            print(f"by {by} and path {path}", "\n\n")
            WebDriverWait(self.driver, self.wait()).until(
                EC.presence_of_element_located((by, path)))

            # 2. Find element(s) by...
            if many:
                return self.driver.find_elements(by, path)
            return self.driver.find_element(by, path)
        except TimeoutException:
            raise Exception(f"Element {path} was not found by {by}")

    def actions_chain(self, navigation_command: NavigationCommand, elements: Union[list[WebElement], WebElement]):
        for action in navigation_command.actions:
            if action == '':
                continue

            # Extracts action and paramter if available
            _action = action.split('|')
            action = _action[0]

            try:
                param = _action[1]
            except:
                param = None

            # Logs
            print(navigation_command.human_label,
                  action, f"param: {param}", "\n")

            if action == 'create_entry':
                elements_length = len(elements)
                for idx, element in enumerate(elements):

                    if param:
                        value = element.get_attribute(param)
                    else:
                        value = element.text

                    if len(self.data) < elements_length:
                        self.data.append(
                            {navigation_command.human_label: value})
                    else:
                        self.data[idx].update(
                            {navigation_command.human_label: value})

            elif action == 'perform_create_entry':

                # Create tasks in small batches
                for items in self.batch(self.data):
                    current_app.send_task(
                        name='fancy_web_scrapping.webscraper.tasks.create_entry',
                        kwargs={'model_name': navigation_command.model_name,
                                'data': items, **navigation_command.model_kwargs}
                    )

                # Clean data in memory to allow other actions collect more data
                self.data = []

            elif action == 'send_special_key':
                self.__param_is_required(
                    action=action,
                    method=self.actions.sendKeys(getattr(Keys, param)),
                    param=param
                )

            # elif action == 'move_to_element_with_offset':
            #     self.actions.move_by_offset(8, 0)
            #     self.actions.pause(self.wait())

            #     offset = self.human.wind_mouse(8, 0, elements)

            #     self.actions.move_to_element_with_offset(
            #         elements, offset[0], offset[1])
            #     # Schedule pause action of [t] seconds
            #     self.actions.pause(self.wait())

            elif action == 'scroll_page':
                Humanizer.scroll_page(elements)

            elif action == 'back':
                self.driver.execute_script("window.history.go(-1)")

            elif action == 'perform_actions':
                # 4. Perform actions from the ActionChain
                self.actions.perform()

            elif action == 'debug_print_data':
                print(self.data)

            else:
                getattr(self.actions, action)(elements)
                # Schedule pause action of [t] seconds
                self.actions.pause(self.wait())

    def start(self) -> None:
        def _():
            self.driver.get(self.url)

            self.actions.pause(self.wait())

            for navigation_command in self.navigation_guide:
                print("NAVIGATION COMMAND")

                if navigation_command.path:
                    element_s = self.find_element_by(navigation_command.by,
                                                     navigation_command.path,
                                                     many=navigation_command.many)

                    self.actions_chain(navigation_command, element_s)

                if navigation_command.subcommands:
                    for subcommand in navigation_command.subcommands:
                        print("NAVIGATION SUBCOMMAND")
                        element_s = self.find_element_by(
                            subcommand.by, subcommand.path, many=subcommand.many)

                        self.actions_chain(subcommand, element_s)

        self.__on_error(_)

    def quit(self, sleep_seconds: int = 0) -> None:
        sleep(sleep_seconds)
        self.driver.quit()
