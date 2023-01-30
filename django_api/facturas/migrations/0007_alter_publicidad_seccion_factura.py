# Generated by Django 4.1.3 on 2023-01-30 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0006_publicidad_nombre_alter_publicidad_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicidad',
            name='seccion_factura',
            field=models.CharField(choices=[('A', 'Seccion A'), ('B', 'Seccion B'), ('C', 'Seccion C'), ('OTRO', 'Otro')], default='A', max_length=4, verbose_name='Seccion Factura'),
        ),
    ]
