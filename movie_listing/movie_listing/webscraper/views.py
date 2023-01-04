from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from ..sources.serializers import SourceSerializer
from ..sources.models import Source


class WebScraperViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows scrapy movie data from a source (website).
    """
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    
    def retrieve(self, request, *args, **kwargs):
        return Response({"data": "test"})