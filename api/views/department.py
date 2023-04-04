from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers.department import DepartmentSerializer
from api.models.department import DepartmentModel


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DepartmentSerializer
    queryset = DepartmentModel.objects.all()
