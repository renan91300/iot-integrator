from django.db import models
from api.models.base import BaseModel
from api.models.location import LocationModel
from api.models.category import Category
from api.models.project import Project


class DeviceModel(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nome")
    location = models.ForeignKey(
        LocationModel, on_delete=models.PROTECT, verbose_name="Localização"
    )
    status = models.JSONField(verbose_name="Status")
    config = models.JSONField(verbose_name="Configuração do dispositivo")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Categoria", related_name="devices"
    )
    received_data_config = models.JSONField(
        verbose_name="Configuração de dados recebidos"
    )
    project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name="Projeto")

    def __str__(self):
        return f"{self.name} - {self.location}"

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
