import importlib

from celery import shared_task
# from celery.utils.log import get_task_logger

from .spiders.ingresso_dot_com import IngressoDotCom
from .spiders.chrome_driver import ChromeDriver

# logger = get_task_logger(__name__)


@shared_task
def scrap_movies(source):

    navigation_guide = None

    # DEFINE INSTRUCTIONS
    if source['name'] == 'ingresso.com':
        navigation_guide = IngressoDotCom()
        navigation_guide.go_to_theaters_list()
        navigation_guide.get_and_record_movie_theaters()
        # navigation_guide.get_movies()

    # EXECUTE INSTRUCTIONS
    if navigation_guide:
        website = ChromeDriver(
            url=source['url'],
            navigation=navigation_guide,
        )

        website.start()
        website.quit(sleep_seconds=10)


@shared_task
def create_entry(model_name: str, data: list[dict]):
    module = None

    # import the Model class
    if model_name == 'Place':
        module = importlib.import_module('movie_listing.places.models')
    elif model_name == 'Movie':
        module = importlib.import_module('movie_listing.movies.models')

    # Insert value
    if module:
        model = getattr(module, model_name)
        model.objects.bulk_create([model(**entry) for entry in data])
