from rest_framework import serializers
from api.models.device import DeviceModel
from api.models.location import LocationModel
from api.models.category import Category


class DeviceSerializer(serializers.ModelSerializer):
    status = serializers.JSONField()
    config = serializers.JSONField()
    received_data_config = serializers.JSONField()
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=LocationModel.objects.all(), source="location", write_only=True
    )
    location_name = serializers.SlugRelatedField(
        source="location", slug_field="name", read_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    category_name = serializers.SlugRelatedField(
        source="category", slug_field="name", read_only=True
    )

    class Meta:
        model = DeviceModel
        fields = [
            "id",
            "name",
            "status",
            "config",
            "received_data_config",
            "location_id",
            "location_name",
            "category_id",
            "category_name",
            "project",
        ]
