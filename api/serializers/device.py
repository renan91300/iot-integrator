from rest_framework import serializers
from api.models.device import DeviceModel

class DeviceSerializer(serializers.ModelSerializer):
    status = serializers.JSONField()
    config = serializers.JSONField()
    received_data_config = serializers.JSONField()

    class Meta:
        model = DeviceModel
        fields = "__all__"