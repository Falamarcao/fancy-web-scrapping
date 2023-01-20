import traceback
from time import sleep
from typing import Union, Callable

from selenium.webdriver import Remote, ChromeOptions

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException

from .our_action_chains import OurActionChains
from ..navigator.navigation_guide import NavigationGuide
from ..navigator.navigation_command import NavigationCommand


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
        self.webdriver_wait = WebDriverWait(self.driver, 20)
        self.action_chains: OurActionChains = OurActionChains(self.driver)

    @staticmethod
    def __on_error(method: Callable) -> None:
        try:
            method()
        except Exception as e:
            print("\n\n", "-"*10, "\n", str(e), "\n",
                  traceback.format_exc(), "-"*10, "\n\n")

    def find_element_by(self, by, path, many: bool, popup: bool = False) -> Union[list[WebElement], WebElement]:
        try:
            # 1. Wait for element presence
            print(f"by {by} and path {path}", "\n\n")
            self.webdriver_wait.until(
                EC.presence_of_element_located((by, path)))  # timeout 20 seconds

            # 2. Find element(s) by...
            if many:
                return self.driver.find_elements(by, path)
            return self.driver.find_element(by, path)
        except TimeoutException:
            if not popup:
                raise Exception(f"Element {path} was not found by {by}")

    def schedule_actions(self, navigation_command: NavigationCommand, elements: Union[list[WebElement], WebElement], **kwargs):
        """
        Schedules actions using Selenium's ActionChains and executes some custom actions.
        """

        if navigation_command.actions:
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
                if param:
                    print(navigation_command.human_label,
                          action, f"param: {param}", "\n")
                else:
                    print(navigation_command.human_label, action, "\n")

                # Schedules actions
                if action == 'scrap_data':
                    self.action_chains.add_action(
                        action,
                        elements=elements,
                        label=navigation_command.human_label,
                        param=param,
                        many=navigation_command.many,
                        **kwargs.get('kwargs_scrap_data', {})
                    )

                elif action == 'create_entry':
                    self.action_chains.add_action(
                        action,
                        model_name=navigation_command.model_name,
                        **navigation_command.model_kwargs
                    )

                elif action == 'send_special_key':
                    self.action_chains.add_action(action, param=param)

                elif action == 'slow_typing':
                    self.action_chains.add_action(action, text=param)

                elif action == 'scroll_page':
                    self.action_chains.add_action(
                        action, on_element_s=elements)

                elif action == 'perform_actions':
                    self.action_chains.perform_actions()

                elif action == 'debug_print_data':
                    self.action_chains.add_action(action)

                else:
                    self.action_chains.add_action(action, elements)

    def exec(self, navigation_command: NavigationCommand, **kwargs):
        element_or_elements = self.find_element_by(navigation_command.by,
                                                   navigation_command.path,
                                                   many=navigation_command.many,
                                                   popup=navigation_command.popup)

        self.schedule_actions(navigation_command,
                              element_or_elements, **kwargs)

    def exec_sub(self, navigation_command: NavigationCommand, **kwargs):
        for subcommand in navigation_command.subcommands:
            print("NAVIGATION SUBCOMMAND")
            self.exec(subcommand, **kwargs)

    def with_many(self, navigation_command: NavigationCommand):
        """
        Parent has [subcommands] and [many = True]
        """

        elements = self.find_element_by(navigation_command.by,
                                        navigation_command.path,
                                        many=navigation_command.many,
                                        popup=navigation_command.popup)
        
        print("with_many", f"path: {navigation_command.path}", [e.get_attribute('href') for e in elements])

        for idx, element in enumerate(elements):
            # Execute/Schedule all the subcommands for each element
            self.exec_sub(navigation_command=navigation_command,
                          **{'kwargs_scrap_data': {'parent_index': idx}})

    def define_path(self, navigation_command: NavigationCommand):
        """
        Defines the path to schedule and execute actions
        A command with children means that the command parent wil bring
        the children together on the same path.
        """
        print("NAVIGATION COMMAND")

        if navigation_command.many and navigation_command.subcommands:
            # for _ in range(0, 5):
            self.with_many(navigation_command)
                # self.action_chains.add_action(navigation_command.next)
        else:
            if navigation_command.path:
                self.exec(navigation_command)

            if navigation_command.subcommands:
                self.exec_sub(navigation_command)

    def start(self) -> None:
        def _():
            self.driver.get(self.url)

            for navigation_command in self.navigation_guide:
                self.define_path(navigation_command)

        self.__on_error(_)

    def quit(self, sleep_seconds: int = 0) -> None:
        sleep(sleep_seconds)
        self.driver.quit()
