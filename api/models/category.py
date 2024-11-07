from django.db import models
from api.models.base import BaseModel
from api.models.project import Project


class Category(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Nome")
    base_settings = models.JSONField(verbose_name="Configuração base")
    project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name="Projeto")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
