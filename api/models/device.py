from django.db import models
from api.models.base import BaseModel
from api.models.location import LocationModel
from api.models.academic import AcademicModel
from api.models.category import Category


class DeviceModel(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nome")
    location = models.ForeignKey(
        LocationModel, on_delete=models.PROTECT, verbose_name="Localização"
    )
    settings = models.JSONField(verbose_name="Configurações")
    # No settings poderia ter, por exemplo, uma configuração status,
    # indicando se a fechadura está aberta ou fechada nos dispositivos
    # específicos para essa finalidade
    academics = models.ManyToManyField(
        AcademicModel,
        through="DeviceAcademicsModel",
        blank=True,
        help_text="Membros com permissões de acesso",
        verbose_name="Acadêmico",
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Categoria"
    )

    def __str__(self):
        return f"{self.name} - {self.location}"

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
