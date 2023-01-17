from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from .exceptions import ValidationError
from ..sources.serializers import SourceSerializer
from ..sources.models import Source
from .tasks import scrap_source


class WebScraperViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows scrap data from a source (website).

    endpoint: /api/v1/webscraper?id={integer}

    Selenium Grid: http://localhost:4444/
    """
    queryset = Source.objects.values()
    serializer_class = SourceSerializer

    def get_queryset(self, *args, **kwargs):
        _id = self.request.query_params.get('id')

        if not _id:
            raise ValidationError

        return self.queryset.filter(pk=_id)

    def retrieve(self, request, *args, **kwargs) -> None:
        if self.kwargs.get('pk'):
            raise ValidationError

    def list(self, request, *args, **kwargs) -> Response:
        _id = self.request.query_params.get('id')

        if not _id:
            raise ValidationError

        source = self.queryset.filter(pk=_id)[0]
        task = scrap_source.delay(source)
        return Response({"status": "OK", "input": source, "task_id": task.id})
