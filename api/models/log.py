from djongo import models
from api.models.base import BaseModel
from api.models.device import DeviceModel
from api.models.academic import AcademicModel


class LogModel(BaseModel):
    device = models.ForeignKey(DeviceModel, on_delete=models.PROTECT)
    employee = models.ForeignKey(AcademicModel, on_delete=models.PROTECT, null=True)
    log = models.JSONField()
