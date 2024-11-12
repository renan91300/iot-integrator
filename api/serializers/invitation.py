from rest_framework import serializers
from api.models.project import Project

from api.models.invitation import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    def validate_project(self, value):
        project = Project.objects.filter(id=value.id)
        if project.filter(members=self.context["request"].user.id):
            return value
        raise serializers.ValidationError("You can't invite to this project")

    class Meta:
        model = Invitation
        fields = ("email", "name", "project")