from rest_framework import serializers
from api.models.log import LogModel


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogModel
        fields = "__all__"
