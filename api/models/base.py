from django.db import models


class BaseModel(models.Model):
    """
    Esse modelo base contêm informações que podem ser herdadas por diversos outros modelos.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
