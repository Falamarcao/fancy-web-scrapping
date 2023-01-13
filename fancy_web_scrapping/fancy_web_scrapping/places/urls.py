from rest_framework.routers import SimpleRouter
from .views import PlaceViewSet

app_name = 'places'

router = SimpleRouter()
router.register(r'places', PlaceViewSet, basename='places')
