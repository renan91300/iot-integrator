from django.forms import ValidationError
from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.conf import settings

from accounts.models import UserAccount
from api.models.invitation import Invitation

class UserViewSet(DjoserUserViewSet):

    def get_queryset(self):
        user = self.request.user
        queryset = UserAccount.objects.all()
        if settings.HIDE_USERS and (self.action in ["update", "partial_update", "list", "retrieve"]) and not user.is_staff:
            queryset = queryset.filter(clientId = user.clientId)
        return queryset
    
    def perform_create(self, serializer, *args, **kwargs):
        # check if the email has a pending invitation
        # otherwise raise an error
        email = serializer.validated_data.get('email')
        invitation = Invitation.objects.filter(email=email, accepted=False).first()
        if not invitation:
            raise ValidationError('No invitation found for this email')
        
        invitation.accepted = True
        invitation.save()
        super().perform_create(serializer, *args, **kwargs)


