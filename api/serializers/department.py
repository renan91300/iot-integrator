from rest_framework import serializers

from api.models.department import DepartmentModel


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentModel
        fields = "__all__"
