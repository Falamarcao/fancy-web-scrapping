from rest_framework.routers import APIRootView, DefaultRouter

from .users.urls import router as users_router
from .sources.urls import router as sources_router
from .places.urls import router as places_router
from .movies.urls import router as movies_router
from .webscraper.urls import router as webscraper_router


class FancyWebScrapping(APIRootView):
    """
    The project focus on scrapping data from any website
    by using simple JSON (dict) instructions (commands).
    """
    pass


class DocumentedRouter(DefaultRouter):
    APIRootView = FancyWebScrapping


router = DocumentedRouter()
router.registry.extend(users_router.registry)
router.registry.extend(sources_router.registry)
router.registry.extend(places_router.registry)
router.registry.extend(movies_router.registry)
router.registry.extend(webscraper_router.registry)
