from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models.device import DeviceModel
from api.serializers.device import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer
    queryset = DeviceModel.objects.all()
