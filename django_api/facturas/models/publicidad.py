"""Publicidad model."""


"""
El código define un modelo de Django llamado "Publicidad". La clase "Publicidad" hereda de la clase 
"DateBaseModel" que proporciona campos adicionales como fecha de creación y modificación.

El modelo "Publicidad" tiene los siguientes campos:

"nombre": un campo de texto opcional para el nombre de la publicidad.
"fecha_vigencia_inicio": fecha y hora de inicio de la vigencia de la publicidad.
"fecha_vigencia_fin": fecha y hora de finalización de la vigencia de la publicidad.
"valor": valor pagado por la publicidad.
"imagen": imagen de la publicidad que se almacena en el sistema de archivos del servidor en la ubicación
 especificada.
"seccion_factura": una opción para la sección de la factura en la que aparecerá la publicidad.
"is_active": un campo booleano que indica si la publicidad está activa o no.
El campo "seccion_factura" utiliza la clase "SeccionFacturaChoices" para definir las opciones de 
selección disponibles. Las opciones son 'A', 'B', 'C' y 'OTRO'. El campo "is_active" tiene un valor 
predeterminado de "True" para indicar que la publicidad está activa.

Además, el modelo tiene un método "str" que devuelve el nombre del modelo y su ID para una representación
 legible del modelo. La clase "Meta" se utiliza para proporcionar metadatos del modelo, como el nombre
de la tabla y el nombre en singular y plural.

"""
# Django
from django.db import models

# Utilities
from django_api.utils.models import DateBaseModel


class SeccionFactura(DateBaseModel):

    class SeccionFacturaChoices(models.TextChoices):
        SECCION_A = 'A'
        SECCION_B = 'B'
        SECCION_C = 'C'
        OTRO = 'OTRO'

    seccion_factura = models.CharField(
        'Seccion Factura',
        choices=SeccionFacturaChoices.choices,
        max_length=4
    )
    valor = models.FloatField('Valor', help_text="Valor definido para la sección.")

    def __str__(self):
        return "SeccionFactura {}".format(self.id)

    class Meta(DateBaseModel.Meta):
        db_table = 'seccion_factura'
        managed = True
        verbose_name = 'seccion_factura'
        verbose_name_plural = 'secciones de factura'


class Publicidad(DateBaseModel):
    
    class SeccionFacturaChoices(models.TextChoices):
        SECCION_A = 'A'
        SECCION_B = 'B'
        SECCION_C = 'C'
        OTRO = 'OTRO'

    nombre = models.CharField('Nombre', max_length=250, null=True, blank=True)
    fecha_vigencia_inicio = models.DateTimeField('Fecha inicio de vigencia')
    fecha_vigencia_fin = models.DateTimeField('Fecha fin de vigencia')
    valor = models.FloatField('Valor', help_text="Valor pagado por la publicidad", default=0)
    imagen = models.ImageField('Imagen', upload_to ='uploads/publicidad/%Y/%m/%d/')
    seccion_factura = models.CharField(
        'Seccion Factura',
        choices=SeccionFacturaChoices.choices,
        max_length=4,
        default=SeccionFacturaChoices.SECCION_A
    )
    is_active = models.BooleanField('Estado', default=True)
    seccionfactura = models.ForeignKey(SeccionFactura, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Publicidad {}".format(self.id)

    class Meta(DateBaseModel.Meta):
        db_table = 'publicidad'
        managed = True
        verbose_name = 'publicidad'
        verbose_name_plural = 'publicidades'


