from celery import shared_task
from celery.utils.log import get_task_logger

from .spiders.chrome_driver import ChromeDriver
from .spiders.navigator.navigation_guide import NavigationGuide


# logger = get_task_logger(__name__)

@shared_task
def scrap_movies(source):

    navigation = None

    # DEFINE INSTRUCTIONS
    if source['name'] == 'ingresso.com':

        navigation_guide = NavigationGuide()

        navigation_guide.append({
            'human_label': 'button_cookies_OK',
            'actions': ['move_to_element', 'click',],
            'XPATH': r'//*[@id="c-p-bn"]'
        })

        navigation_guide.append({
            'human_label': 'button_sao_paulo_continuar',
            'actions': ['move_to_element', 'click',],
            'XPATH': r'//*[@id="hd-local-suggest"]/div/div/form/div/button[1]'
        })

        navigation_guide.append({
            'human_label': 'menu_option_cinemas',
            'actions': ['move_to_element', 'click',],
            'CLASS_NAME': r'card-theater'
        })

    # EXECUTE INSTRUCTIONS
    if navigation_guide:
        website = ChromeDriver(url=source['url'], navigation=navigation_guide)
        website.start()
        website.quit(sleep_seconds=20)
