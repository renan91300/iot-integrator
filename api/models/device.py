from djongo import models
from api.models.base import BaseModel
from api.models.location import LocationModel
from api.models.academic import AcademicModel


class DeviceModel(BaseModel):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(LocationModel, on_delete=models.PROTECT)
    settings = models.JSONField()
    # No settings poderia ter, por exemplo, uma configuração status,
    # indicando se a fechadura está aberta ou fechada nos dispositivos
    # específicos para essa finalidade
    academics = models.ManyToManyField(
        AcademicModel, blank=True, help_text="Membros com permissões de acesso"
    )
