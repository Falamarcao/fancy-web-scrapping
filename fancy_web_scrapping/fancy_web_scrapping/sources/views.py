from rest_framework.viewsets import ModelViewSet
from .serializers import SourceSerializer
from .models import Source


class SourceViewSet(ModelViewSet):
    """
    API endpoint that allows...
    """
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    # permission_classes = []    
