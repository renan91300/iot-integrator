from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.serializers.invitation import InvitationSerializer
from api.models.invitation import Invitation
from api.models.project import Project
from tasks import send_invitation_email

class InvitationViewSet(viewsets.GenericViewSet):
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all()

    def get_serializer_context(self):
        # pass the request object to the serializer
        return {"request": self.request}
    
    def get_serializer(self, *args, **kwargs):
        # pass the request object to the serializer
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get_permissions_classes(self):
        if self.action == 'accept':
            return [AllowAny]
        return [IsAuthenticated]

    def create(self, request):
        data = request.data
        data["invited_by"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(invited_by=request.user)
        
        send_invitation_email.delay(
            email=serializer.validated_data['email'],
            token=serializer.instance.token,
            is_project_invitation=serializer.validated_data.get('project') is not None
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(detail=False, methods=['post'])
    def accept(self, request):
        token = request.data.get("token")        
        # check if the invitation exists
        invitation = get_object_or_404(Invitation, token=token, accepted=False)

        # if the user has already an account, the invitation is accept and return success
        # if the user don't have an account, the user is redirect to register page
        user = get_user_model().objects.filter(email=invitation.email).first()
        if user:
            invitation.accepted = True
            invitation.save()

            if invitation.project:
                project = Project.objects.filter(id=invitation.project.id).first()
                project.members.add(user)
                project.save()

            return Response(status=status.HTTP_200_OK)
        else:
            # the frontend will check the status and if is 302 should redirect to register page             
            return Response(status=status.HTTP_302_FOUND)