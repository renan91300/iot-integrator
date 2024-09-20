from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.serializers.invitation import InvitationSerializer
from api.models.invitation import Invitation
from tasks import send_invitation_email

class InvitationViewSet(viewsets.GenericViewSet):
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['accept']:
            return [AllowAny]
        return super().get_permissions()

    def create(self, request):
        data = request.data
        data["invited_by"] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(invited_by=request.user)
        
        send_invitation_email.delay(
            email=serializer.validated_data['email'],
            token=serializer.instance.token,
            is_project_invitation=serializer.validated_data.get('project') is not None
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(detail=True, methods=['post'])
    def accept(self, request, token):        
        # check if the invitation exists
        invitation = get_object_or_404(Invitation, token=token, accept=False)

        # if the user has already an account, the invitation is accept and return success
        # if the user don't have an account, the user is redirect to register page
        if get_user_model().objects.get(email=invitation.email):
            invitation.accepted = True
            invitation.save()
            return Response(status=status.HTTP_200_OK)
        else:
            # the frontend will check the status and if is 302 should redirect to register page             
            return Response(status=status.HTTP_302_FOUND)