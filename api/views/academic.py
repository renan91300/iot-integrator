from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models.academic import AcademicModel
from api.serializers.academic import AcademicSerializer


class AcademicViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AcademicSerializer
    queryset = AcademicModel.objects.all()
