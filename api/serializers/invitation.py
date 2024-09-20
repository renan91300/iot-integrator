from rest_framework import serializers

from api.models.invitation import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ("email", "project")