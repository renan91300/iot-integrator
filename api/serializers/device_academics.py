from rest_framework import serializers
from api.serializers.device import DeviceSerializer
from api.serializers.academic import AcademicSerializer

from api.models.device_academics import DeviceAcademicsModel, AccessPeriodModel, TimeIntervalModel

class TimeIntervalSerializer(serializers.ModelSerializer):
    start = serializers.CharField(max_length=5)
    end = serializers.CharField(max_length=5)

    class Meta:
        model = TimeIntervalModel
        fields = "__all__"

class AccessPeriodSerializer(serializers.ModelSerializer):
    day_of_week = serializers.IntegerField()
    time_intervals = TimeIntervalSerializer(many=True)

    class Meta:
        model = AccessPeriodModel   
        fields = "__all__"

class DeviceAcademicsSerializer(serializers.ModelSerializer):
    access_period = AccessPeriodSerializer(many=True)

    class Meta:
        model = DeviceAcademicsModel
        fields = "__all__"
