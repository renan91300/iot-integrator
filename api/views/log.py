from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models.log import LogModel
from api.serializers.log import LogSerializer


class LogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LogSerializer
    queryset = LogModel.objects.all()
