from time import sleep
from random import uniform, uniform

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

import numpy as np


class Humanizer:

    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver
        self.sqrt3 = np.sqrt(3)
        self.sqrt5 = np.sqrt(5)

    @staticmethod
    def slow_typing(element: WebElement, text: str):
        """
        The slow typing function requires pageInput or the words that need to be typed,
        and the element in which they need to be sent through. Each letter of the string
        of words is iterated through and typed into the element with realistic typing speeds.
        
        Args:
            element: page element to be typed
            pageInput: text to be typed
            
        Ref:
            https://www.binarydefense.com/mimicking-human-activity-using-selenium-and-python/
        """
        for letter in text:
            sleep(float(uniform(.05, .3)))
            element.send_keys(letter)

    @staticmethod
    def scroll_page(driver: WebDriver, elements: list[WebElement]):
        """
        Shake the mouse as scrolling occurs
        
        Args:
            driver: Selenium driver
            elements: list of Selenium elements
        
        Ref:
            https://www.binarydefense.com/mimicking-human-activity-using-selenium-and-python/
        """
        for _ in elements:
            driver.execute_script(
                "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});")
            sleep(0.3)

    def wind_mouse(self, start_x, start_y, element: WebElement, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=lambda x, y: None):
        '''
        WindMouse algorithm. Calls the move_mouse kwarg with each new step.
        Released under the terms of the GPLv3 license.
        G_0 - magnitude of the gravitational fornce
        W_0 - magnitude of the wind force fluctuations
        M_0 - maximum step size (velocity clip threshold)
        D_0 - distance where wind behavior changes from random to damped
        '''
        current_x, current_y = start_x, start_y
        v_x = v_y = W_x = W_y = 0
        while (dist := np.hypot(element.location["x"]-start_x, element.location["y"]-start_y)) >= 1:
            W_mag = min(W_0, dist)
            if dist >= D_0:
                W_x = W_x/self.sqrt3 + \
                    (2*np.random.random()-1)*W_mag/self.sqrt5
                W_y = W_y/self.sqrt3 + \
                    (2*np.random.random()-1)*W_mag/self.sqrt5
            else:
                W_x /= self.sqrt3
                W_y /= self.sqrt3
                if M_0 < 3:
                    M_0 = np.random.random()*3 + 3
                else:
                    M_0 /= self.sqrt5
            v_x += W_x + G_0*(element.location["x"]-start_x)/dist
            v_y += W_y + G_0*(element.location["y"]-start_y)/dist
            v_mag = np.hypot(v_x, v_y)
            if v_mag > M_0:
                v_clip = M_0/2 + np.random.random()*M_0/2
                v_x = (v_x/v_mag) * v_clip
                v_y = (v_y/v_mag) * v_clip
            start_x += v_x
            start_y += v_y
            move_x = int(np.round(start_x))
            move_y = int(np.round(start_y))
            if current_x != move_x or current_y != move_y:
                # This should wait for the mouse polling interval
                move_mouse(current_x := move_x, current_y := move_y)
        return current_x, current_y
