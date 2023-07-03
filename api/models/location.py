from djongo import models
from api.models.base import BaseModel


class LocationModel(BaseModel):
    """
    Modelo que representa localizações dentro do campus
    """

    name = models.CharField(max_length=120)
    block = models.CharField(max_length=120)
    floor = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name="Localização"
        verbose_name_plural="Localizações"
