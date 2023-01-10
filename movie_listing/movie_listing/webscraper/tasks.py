import importlib

from celery import shared_task
# from celery.utils.log import get_task_logger

from .spiders.chrome_driver import ChromeDriver
from selenium.webdriver.remote.webelement import WebElement
from .spiders.navigator.navigation_guide import NavigationGuide
from .spiders.navigator.navigation_command import NavigationCommand

# logger = get_task_logger(__name__)


@shared_task
def scrap_movies(source):

    navigation = None

    # DEFINE INSTRUCTIONS
    if source['name'] == 'ingresso.com':

        navigation_guide = NavigationGuide()

        # Close cookies popup window
        navigation_guide.append({
            'human_label': 'button_cookies_OK',
            'actions': ['move_to_element', 'click',],
            'XPATH': r'//*[@id="c-p-bn"]'
        })

        # Move to menu item and click
        navigation_guide.append({
            'human_label': 'button_sao_paulo_continuar',
            'actions': ['move_to_element', 'click',],
            'XPATH': r'//*[@id="hd-local-suggest"]/div/div/form/div/button[1]'
        })

        navigation_guide.append({
            'human_label': 'menu_cinema',
            'actions': ['move_to_element', 'click', 'perform_actions'],
            'XPATH': r'//*[@id="header"]/div[2]/div/div/div/nav/ul/li[2]/a'
        })

        # GET PLACES

        # place names
        navigation_guide.append({
            'human_label': 'Place',
            'actions': [],
            'subcommands': [
                {'actions': ['scroll_page'],
                 'many': True,
                 'XPATH': r'//div'},
                {'human_label': 'name',
                 'actions': ['create_entry'],
                 'many': True,
                 'XPATH': r'//div[contains(@class, "card-theater-text")]//strong'},
                {'human_label': 'address',
                 'model_name': 'Place',
                 'actions': ['create_entry', 'perform_create_entry'],
                 'many': True,
                 'XPATH': r'//div[contains(@class, "card-theater-text")]//span'}
            ]
        })

        # # Navigation (clicks)
        # navigation_guide.append({
        #     'human_label': 'Place',
        #     'actions': ['move_to_element',  'click',],
        #     'many': True,
        #     'XPATH': r'//li[contains(@class,"card-theater")]'
        # })

    # EXECUTE INSTRUCTIONS
    if navigation_guide:
        website = ChromeDriver(
            url=source['url'],
            navigation=navigation_guide,
        )

        def transform(human_label: str, elements: WebElement):
            data: dict = {}

            for element in elements:

                if human_label == 'Place':
                    data = {
                        'name': name,
                        'address': address,
                        'url': url
                    }
                elif human_label == 'Movie':
                    data = {
                        'source': source,
                        'place': place,
                        'url': url,
                        'name': name,
                        'description': description,
                        'duration': duration,
                        'sessions': sessions
                    }

            return data

        website.transform = transform
        website.start()
        website.quit(sleep_seconds=10)


@shared_task
def create_entry(model_name, data):
    module = None

    # import the Model class
    if model_name == 'Place':
        module = importlib.import_module('movie_listing.places.models')
    elif model_name == 'Movie':
        module = importlib.import_module('movie_listing.movies.models')

    # Insert value
    if module:
        m = getattr(module, model_name)(**data)
        # FIXME: check if is necessary the force_insert
        m.save(force_insert=True)
