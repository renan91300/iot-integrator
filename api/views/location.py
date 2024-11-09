from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.serializers.location import LocationSerializer
from api.models.location import LocationModel


class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer
    queryset = LocationModel.objects.all()

    def get_queryset(self):
        project_id = self.request.GET.get("project_id")
        queryset = self.queryset.filter(project=project_id, project__members=self.request.user.id)
        return queryset