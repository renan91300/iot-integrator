from django.db import models
from django.utils.crypto import get_random_string
from api.models.base import BaseModel
from api.models.project import Project
from accounts.models import UserAccount

class Invitation(BaseModel):
    email = models.EmailField()
    name = models.CharField(max_length=255, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name='invitations')
    invited_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    token = models.CharField(max_length=64, unique=True, default=get_random_string(64))

    def __str__(self):
        return f"Convite para {self.email} em {self.project}"