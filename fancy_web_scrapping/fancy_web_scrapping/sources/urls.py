from rest_framework.routers import SimpleRouter
from .views import SourceViewSet

app_name = 'sources'

router = SimpleRouter()
router.register(r'source', SourceViewSet, basename='sources')
