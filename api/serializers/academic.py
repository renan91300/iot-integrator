from rest_framework import serializers
from api.models.academic import AcademicModel


class AcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicModel
        fields = "__all__"
