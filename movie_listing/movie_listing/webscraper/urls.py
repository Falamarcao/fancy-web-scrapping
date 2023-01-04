from rest_framework.routers import SimpleRouter
from .views import WebScraperViewSet

app_name = 'webscraper'

router = SimpleRouter()
router.register(r'webscraper', WebScraperViewSet, basename='webscraper')
