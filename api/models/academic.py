from djongo import models
from api.models.base import BaseModel
from api.models.department import DepartmentModel


class AcademicModel(BaseModel):
    """
    Classe modelo que representa a comunidade acadêmica do campus,
    seja professor, servidor, aluno, etc.
    """

    name = models.CharField(max_length=255, verbose_name="Nome")
    registration = models.CharField(max_length=30, verbose_name="Matrícula")
    department = models.ForeignKey(
        DepartmentModel,
        on_delete=models.PROTECT,
        verbose_name="Departamento/Coordenadoria",
    )
    key = models.CharField(max_length=16, help_text="Hash identificador do funcionário")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Acadêmico"
        verbose_name_plural = "Acadêmicos"