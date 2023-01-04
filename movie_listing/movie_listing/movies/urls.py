from rest_framework.routers import SimpleRouter
from .views import MovieViewSet

app_name = 'movies'

router = SimpleRouter()
router.register(r'movies', MovieViewSet, basename='movies')
