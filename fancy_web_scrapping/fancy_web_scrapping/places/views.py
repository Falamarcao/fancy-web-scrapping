from rest_framework.viewsets import ModelViewSet
from .serializers import PlaceSerializer
from .models import Place


class PlaceViewSet(ModelViewSet):
    """
    API endpoint that allows...
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    # permission_classes = []
