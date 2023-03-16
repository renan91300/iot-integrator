from rest_framework import serializers
from api.models.location import LocationModel


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationModel
        fields = "__all__"
