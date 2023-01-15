
# Django
from django.db import models

# Utilities
from .base import DateBaseModel

class Departamentos(DateBaseModel):
    nombre = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.nombre

    class Meta(DateBaseModel.Meta):
        db_table = 'departamentos'
        managed = True
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'