from django.db import models
from api.models.base import BaseModel
from api.models.project import Project

class LocationModel(BaseModel):
    """
    Modelo que representa localizações dentro do campus
    """

    name = models.CharField(max_length=120)
    block = models.CharField(max_length=120)
    floor = models.PositiveSmallIntegerField()
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="locations"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Localização"
        verbose_name_plural = "Localizações"
