from celery import shared_task
from celery.utils.log import get_task_logger

from json import loads

from .spiders.chrome_driver import ChromeDriver


logger = get_task_logger(__name__)


@shared_task
def scrap_movies(source):

    if source['name'] == 'ingresso.com':
        # XPATS leading to the target web page.
        xpaths = ['//*[@id="header"]/div[2]/div/div/div/nav/ul/li[2]/a']
        website = ChromeDriver(url=source['url'], xpath_list=xpaths)
        website.start()
        website.quit(sleep_seconds=5)
