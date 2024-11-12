from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db.models import Value

from api.models.project import Project
from api.serializers.project import ProjectSerializer


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
    
    @action(detail=False, methods=['get'])
    def members(self, request):
        project = request.GET.get("project_id")
        project = self.queryset.filter(id=project).first()

        # Get email and name of project members and invited members in a single dictionary
        members = project.members.annotate(accepted=Value(True)).order_by("-updated_at").values('updated_at', 'email', 'name', 'accepted')
        invited_members = project.invitations.filter(accepted=False).order_by("-updated_at").values('updated_at', 'email', 'name', 'accepted')

        # combine the two querysets as dicts
        members = list(invited_members) + list(members)
        return Response(members)
