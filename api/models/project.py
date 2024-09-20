from django.db import models
from api.models.base import BaseModel
from accounts.models import UserAccount

class Project(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    members = models.ManyToManyField(UserAccount, related_name='projects')

    def __str__(self):
        return self.name