from django.db import models
from api.models.base import BaseModel
from api.models.academic import AcademicModel
from api.models.device import DeviceModel


class DeviceAcademicsModel(BaseModel):
    device = models.ForeignKey(
        DeviceModel, on_delete=models.CASCADE, verbose_name="Dispositivo"
    )
    academic = models.ForeignKey(
        AcademicModel, on_delete=models.PROTECT, verbose_name="Acadêmico"
    )
    access_period = models.JSONField(verbose_name="Período de acesso")

    class Meta:
        verbose_name = "Acadêmico com acesso ao dispositivo"
        verbose_name_plural = "Acadêmicos com acesso ao dispositivo"
