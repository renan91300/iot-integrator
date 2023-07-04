from django.db import models
from api.models.base import BaseModel
from api.models.device import DeviceModel
from api.models.academic import AcademicModel


class LogModel(BaseModel):
    device = models.ForeignKey(DeviceModel, on_delete=models.PROTECT)
    academic = models.ForeignKey(AcademicModel, on_delete=models.PROTECT, null=True)
    log = models.JSONField()

    def __str__(self):
        return f"Log do dispositivo: {self.device}"
