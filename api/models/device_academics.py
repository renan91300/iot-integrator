from djongo import models
from django import forms
from api.models.base import BaseModel
from api.models.academic import AcademicModel
from api.models.device import DeviceModel


class TimeIntervalDefinition(models.Model):
    start = models.CharField(max_length=5)
    end = models.CharField(max_length=5)

    class Meta:
        abstract = True

class TimeIntervalModel(TimeIntervalDefinition):
    pass

class TimeIntervalForm(forms.ModelForm):
    class Meta: 
        model = TimeIntervalModel
        fields = ("start", "end",)
    
class AccessPeriodDefinition(models.Model):
    day_of_week = models.IntegerField()
    time_intervals = models.ArrayField(
        model_container=TimeIntervalDefinition,
        model_form_class=TimeIntervalForm
    )

    class Meta:
        abstract = True

class AccessPeriodModel(AccessPeriodDefinition):
    pass

class AccessPeriodForm(forms.ModelForm):
    class Meta: 
        model = AccessPeriodModel
        fields = ("day_of_week", "time_intervals",)

class DeviceAcademicsModel(BaseModel):
    device = models.ForeignKey(DeviceModel, on_delete=models.PROTECT)
    academic = models.ForeignKey(AcademicModel, on_delete=models.PROTECT)
    access_period = models.ArrayField(
        model_container = AccessPeriodDefinition,
        model_form_class=AccessPeriodForm
    )
    
