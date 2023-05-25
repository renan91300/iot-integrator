from djongo import models
from django import forms
from api.models.base import BaseModel
from api.models.academic import AcademicModel
from api.models.device import DeviceModel


class DeviceAcademicsModel(BaseModel):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    academic = models.ForeignKey(AcademicModel, on_delete=models.PROTECT)
    access_period = models.JSONField()
    
