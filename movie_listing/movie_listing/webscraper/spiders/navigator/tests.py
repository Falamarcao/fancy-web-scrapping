# RUN: docker-compose exec django python manage.py test movie_listing.webscraper.spiders.navigator

import unittest

from selenium.webdriver.common.by import By

from .navigation_command import NavigationCommand
from .navigation_guide import NavigationGuide


class NavigationTestCase(unittest.TestCase):

    navigation_dict = {
        'human_label': 'cinemas',
        'actions': ['click',],
        'XPATH': r'//*[@id="header"]/div[2]/div/div/div/nav/ul/li[2]/a'
    }

    def test_navigation_commands_init_kwargs(self):
        nc = NavigationCommand(
            human_label='cinemas',
            actions=['click'],
            XPATH=r'//*[@id="header"]/div[2]/div/div/div/nav/ul/li[2]/a'
        )

        self.assertEqual(self.navigation_dict['human_label'], nc.human_label)
        self.assertEqual(self.navigation_dict['actions'], nc.actions)
        self.assertEqual(self.navigation_dict['XPATH'], nc.XPATH)

        self.assertIsInstance(nc, NavigationCommand)
        self.assertEqual(self.navigation_dict, nc.to_dict())

        print("OK -> test_navigation_commands_init_kwargs")

    def test_navigation_commands_init_dict(self):
        nc = NavigationCommand(**self.navigation_dict)

        self.assertEqual(self.navigation_dict['human_label'], nc.human_label)
        self.assertEqual(self.navigation_dict['actions'], nc.actions)
        self.assertEqual(self.navigation_dict['XPATH'], nc.XPATH)

        self.assertIsInstance(nc, NavigationCommand)
        self.assertEqual(self.navigation_dict, nc.to_dict())

        print("OK -> test_navigation_commands_init_dict")

    def test_navigation_command_method_by(self):

        ng = NavigationGuide([self.navigation_dict])

        self.assertEqual(ng[0].by, By.XPATH)

        print("OK -> test_navigation_command_method_by")

    def test_navigation_guide_init(self):

        ng = NavigationGuide([self.navigation_dict])

        self.assertEqual(
            self.navigation_dict['human_label'], ng[0].human_label)
        self.assertEqual(self.navigation_dict['actions'], ng[0].actions)
        self.assertEqual(self.navigation_dict['XPATH'], ng[0].XPATH)

        self.assertIsInstance(ng[0], NavigationCommand)
        self.assertIsInstance(ng, NavigationGuide)

        self.assertEqual(ng.first.human_label, ng[0].human_label)
        self.assertEqual(ng.last.human_label, ng[-1].human_label)

        print("OK -> test_navigation_guide_init")

    def test_navigation_guide_append(self):
        ng = NavigationGuide([self.navigation_dict])
        ng.append(self.navigation_dict)

        self.assertEqual(len(ng), 2)

        print("OK -> test_navigation_guide_append")

    def test_navigation_guide_no_attr_error(self):

        ng = NavigationGuide([self.navigation_dict])

        self.assertEqual(ng[0].XPATH, self.navigation_dict['XPATH'])
        self.assertEqual(ng[0].css_selector, None)

        print("OK -> test_navigation_guide_no_attr_error")

    def test_navigation_guide_method_by(self):
        ng = NavigationGuide()

        ng.append({
            'human_label': 'menu_option_cinemas',
            'actions': ['move_to_element', 'click',],
            'XPATH': r'//*[@id="header"]/div[2]/div/div/div/nav/ul/li[2]/a'
        })

        self.assertEqual(ng[0].by, By.XPATH)

        ng.append({
            'human_label': 'cinemas',
            'actions': ['move_to_element', 'click',],
            'CSS_SELECTOR': '.card-theater'
        })

        self.assertEqual(ng[1].by, By.CSS_SELECTOR)

        print("OK -> test_navigation_guide_method_by")


if __name__ == '__main__':
    unittest.main()
