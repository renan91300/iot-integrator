from rest_framework import serializers

from api.models.device_academics import DeviceAcademicsModel

class TimeIntervalSerializer(serializers.Serializer):
    start = serializers.CharField(max_length=5)
    end = serializers.CharField(max_length=5)

class AccessPeriodSerializer(serializers.Serializer):
    day_of_week = serializers.IntegerField()
    time_intervals = TimeIntervalSerializer(many=True)

class DeviceAcademicsSerializer(serializers.ModelSerializer):
    access_period = AccessPeriodSerializer(many=True)

    class Meta:
        model = DeviceAcademicsModel
        fields = "__all__"
