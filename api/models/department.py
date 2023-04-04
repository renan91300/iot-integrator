from djongo import models

from api.models.base import BaseModel
from api.models.location import LocationModel


class DepartmentModel(BaseModel):
    """
    Modelo que representa as coordenadorias
    """

    name = models.CharField(max_length=255, verbose_name="Nome coordenadoria")
    location = models.ForeignKey(LocationModel, on_delete=models.PROTECT)
