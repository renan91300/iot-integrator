from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models.project import Project
from api.serializers.project import ProjectSerializer, ProjectCreateSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(members=self.request.user)

    def perform_create(self, serializer):
        # save the owner and add the owner to the members
        serializer.save(owner=self.request.user)
        serializer.instance.members.add(self.request.user)
        serializer.instance.save()