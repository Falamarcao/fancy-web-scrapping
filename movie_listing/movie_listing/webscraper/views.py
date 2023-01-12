from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from ..sources.serializers import SourceSerializer
from ..sources.models import Source
from .tasks import scrap_movies

from json import dumps


class WebScraperViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows scrapy movie data from a source (website).
    
    Selenium Grid: http://localhost:4444/
    """
    queryset = Source.objects.values()
    serializer_class = SourceSerializer
    
    def retrieve(self, request, *args, **kwargs) -> Response:
        source: dict = self.queryset[0]
        task = scrap_movies.delay(source)

        return Response({"status": "OK", "input": source, "task_id": task.id})
