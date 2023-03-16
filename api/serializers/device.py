from rest_framework import serializers
from api.models.device import DeviceModel


class DeviceSerializer(serializers.ModelSerializer):
    settings = serializers.JSONField()

    class Meta:
        model = DeviceModel
        fields = "__all__"
