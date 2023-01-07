
# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from .base import DateBaseModel

class Ciudades(DateBaseModel):

    nombre = models.CharField(max_length=30, null=False)
    departamento = models.ForeignKey('utils.Departamentos', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta(DateBaseModel.Meta):
        db_table = 'ciudades'
        managed = True
        verbose_name = 'ciudad'
        verbose_name_plural = 'ciudades'