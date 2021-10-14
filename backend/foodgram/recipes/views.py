from rest_framework import viewsets, permissions

from .models import *
from .serializers import *


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny, )


