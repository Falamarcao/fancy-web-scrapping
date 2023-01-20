from time import sleep
from typing import Union, Iterable, Callable
from random import randrange, uniform

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from celery import current_app

class OurActionChains:
    def __init__(self, driver, duration = 500):        
        self.__dir_ActionChains = list(filter(lambda x: x[0] != "_",dir(ActionChains)))
        
        self.action_chains: ActionChains = ActionChains(driver, duration)
        self._actions: list[Union[ActionChains, Callable]] = []
        self.NOT_ACTION_CHAINS = ('scrap_data', 'create_entry',
                               'perform_actions', 'debug_print_data')
        self.data: list[dict] = []
    
    @staticmethod
    def __is_required(action: str, params: Iterable):
        for param in params:
            if not param:
                raise Exception(f"Action {action} requires a parameter")
        
    @staticmethod
    def batch(iterable: Iterable):
        """
        Splits an iterable into multiple batches.    
        """
        l = len(iterable)
        n = round(l/2)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]
    
    @staticmethod
    def wait(start: int = 2, stop: int = 4, step: int = 1):
        return randrange(start=2, stop=4, step=1)
    
    def __getattr__(self, name):
        """
        Method for getting the other methods from ActionChains
        """
        if name in self.__dir_ActionChains:
            def _(*args, **kwargs):
                getattr(self.action_chains, name)(*args, **kwargs)
            return _

        raise AttributeError(name)

    def by_name(self, action: str, *args, **kwargs):
        getattr(self, action)(*args, **kwargs)
        
        return self

    def __set_queue(self):
        """
        Checks if has actions on the self.action_chains,
        append them to the queue (self._actions), and clean
        the ActionChains.
        """
        for device in self.action_chains.w3c_actions.devices:
            encoded = device.encode()
            if encoded["actions"]:
                # If has actions append and reset
                self._actions.append(self.action_chains)
                self.action_chains.reset_actions()
                break
    
    def add_action(self, action: str, *args, **kwargs):
        """
        Add action to the queue (self._actions).
        """
        if action in self.NOT_ACTION_CHAINS:
            print("NOT ACTION CHAINS")
            self.__set_queue()
            # Append Custom Command
            self.by_name(action, *args, **kwargs)
        else:
            print("ACTION CHAINS")
            self.by_name(action, *args, **kwargs)
            self.action_chains.pause(self.wait())
    
    def send_special_key(self, param: str):
        self.__is_required('send_special_key', params=[param])
        self.action_chains.pause(self.wait())
        self.action_chains.send_keys(getattr(Keys, param))
        self.action_chains.pause(self.wait())
        
        return self
    
    def slow_typing(self, text: str):
        self.__is_required('slow_typing', params=[text])
        for letter in text:
            self.action_chains.pause(float(uniform(1.175, 2)))
            self.action_chains.send_keys(letter)
        
        return self
    
    # def wind_mouse(self, start_x, start_y, element: WebElement, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=lambda x, y: None):
    #     '''
    #     WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    #     Released under the terms of the GPLv3 license.
    #     G_0 - magnitude of the gravitational fornce
    #     W_0 - magnitude of the wind force fluctuations
    #     M_0 - maximum step size (velocity clip threshold)
    #     D_0 - distance where wind behavior changes from random to damped
    #     '''
    #     current_x, current_y = start_x, start_y
    #     v_x = v_y = W_x = W_y = 0
    #     while (dist := np.hypot(element.location["x"]-start_x, element.location["y"]-start_y)) >= 1:
    #         W_mag = min(W_0, dist)
    #         if dist >= D_0:
    #             W_x = W_x/self.sqrt3 + \
    #                 (2*np.random.random()-1)*W_mag/self.sqrt5
    #             W_y = W_y/self.sqrt3 + \
    #                 (2*np.random.random()-1)*W_mag/self.sqrt5
    #         else:
    #             W_x /= self.sqrt3
    #             W_y /= self.sqrt3
    #             if M_0 < 3:
    #                 M_0 = np.random.random()*3 + 3
    #             else:
    #                 M_0 /= self.sqrt5
    #         v_x += W_x + G_0*(element.location["x"]-start_x)/dist
    #         v_y += W_y + G_0*(element.location["y"]-start_y)/dist
    #         v_mag = np.hypot(v_x, v_y)
    #         if v_mag > M_0:
    #             v_clip = M_0/2 + np.random.random()*M_0/2
    #             v_x = (v_x/v_mag) * v_clip
    #             v_y = (v_y/v_mag) * v_clip
    #         start_x += v_x
    #         start_y += v_y
    #         move_x = int(np.round(start_x))
    #         move_y = int(np.round(start_y))
    #         if current_x != move_x or current_y != move_y:
    #             # This should wait for the mouse polling interval
    #             move_mouse(current_x := move_x, current_y := move_y)
    #     return current_x, current_y
        
    # def move_to_element_with_offset(self, element: WebElement):
    #     self.move_by_offset(8, 0)
    #     self.pause()

    #     offset = self.human.wind_mouse(8, 0, element)

    #     self.move_to_element_with_offset(element, offset[0], offset[1])
    #     # Schedule pause action of [t] seconds
    #     self.pause()
    
        # return self
    
    def scroll_page(self, on_elements: list[WebElement]):
        def scroll_page_inner():
            for _ in on_elements:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});")
                sleep(0.3)
        
        
        self._actions.append(scroll_page_inner)
        
        return self
    
    # def back(self):
    #     self._driver.execute_script("window.history.go(-1)")
        
    #     return self
    
    def scrap_data(self, elements: Union[list[WebElement], WebElement], label: str, param: str, many: bool = False):
        def scrap_data_inner():
            if many:
                    elements_length = len(elements)
                    for idx, element in enumerate(elements):

                        if param:
                            value = element.get_attribute(param)
                        else:
                            value = element.text

                        if len(self.data) < elements_length:
                            self.data.append({label: value})
                        else:
                            self.data[idx].update({label: value})

            else:
                if param:
                    value = elements.get_attribute(param)
                else:
                    value = elements.text

                self.data.append({label: value})


        self._actions.append(scrap_data_inner)

        return self
    
    def debug_print_data(self):
        self._actions.append(lambda: print(self.data))
        
        return self

    def create_entry(self, model_name: str, **kwargs):
        def create_entry_inner():
            self.__is_required('create_entry', [model_name, kwargs])

            # Create tasks in small batches
            for items in self.batch(self.data):
                current_app.send_task(
                    name='fancy_web_scrapping.webscraper.tasks.create_entry',
                    kwargs={'model_name': model_name,
                            'data': items, **kwargs}
                )

            # Clean data in memory to allow other actions collect more data
            self.data = []


        self._actions.append(create_entry_inner)

        return self
        
    def perform_actions(self):
        for action in self._actions:
            if isinstance(action, ActionChains):
                print("perform_actions - ACTION CHAINS")
                action.perform()
            else:
                print("perform_actions - NOT ACTION CHAINS")
                action()
        
        # self._actions only will be populated,
        # if we had a mix of ActionChains and Custom Commands.
        if self._actions == []:
            self.action_chains.perform()
        
        # Clean actions queue
        self._actions == []
    
    