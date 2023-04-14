# Django
from django.db import models

# Utilities
from django_api.utils.models import DateBaseModel


class Bancos(DateBaseModel):

    nombre = models.TextField('Nombre banco', max_length=150)

    def __str__(self):
        return "Bancos {}".format(self.id)

    class Meta(DateBaseModel.Meta):
        db_table = 'bancos'
        managed = True
        verbose_name = 'banco'
        verbose_name_plural = 'Bancos natha'
