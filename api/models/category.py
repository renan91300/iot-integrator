from api.models.base import BaseModel
from djongo import models


class Category(BaseModel):
    name = models.CharField(max_length=100)
    base_settings = models.JSONField()
