from rest_framework import serializers
from api.models.device import DeviceModel
from api.models.device_academics import DeviceAcademicsModel

from api.serializers.device_academics import DeviceAcademicsSerializer

class DeviceSerializer(serializers.ModelSerializer):
    settings = serializers.JSONField()

    class Meta:
        model = DeviceModel
        fields = "__all__"


class DeviceDetailsSerializer(serializers.ModelSerializer):
    settings = serializers.JSONField()
    academics = serializers.SerializerMethodField()

    class Meta:
        model = DeviceModel
        fields = "__all__"
    
    def get_academics(self, obj):
        device_academics = DeviceAcademicsModel.objects.filter(device=obj)
        return DeviceAcademicsSerializer(device_academics, many=True).data
