from rest_framework import serializers
from api.models.device import DeviceModel


class DeviceSerializer(serializers.ModelSerializer):
    status = serializers.JSONField()
    config = serializers.JSONField()
    received_data_config = serializers.JSONField()
    location = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    
    class Meta:
        model = DeviceModel
        fields = "__all__"

    def get_location(self, obj):
        if obj.location is None:
            return {"id": "", "name": ""}
        return {"id": obj.location.id, "name": obj.location.name}
    
    def get_category(self, obj):
        if obj.category is None:
            return {"id": "", "name": "", "base_settings": {}}
        return {"id": obj.category.id, "name": obj.category.name, "base_settings": obj.category.base_settings}
    

class PostDeviceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = DeviceModel
        fields = "__all__"