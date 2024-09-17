from django.db import models
from api.models.base import BaseModel


class LogModel(BaseModel):    
    log = models.JSONField()
    user = models.ForeignKey(
        "accounts.UserAccount", on_delete=models.PROTECT, verbose_name="Usuário"
    )

    def __str__(self):
        return f"{self.user} - {self.created_at}"