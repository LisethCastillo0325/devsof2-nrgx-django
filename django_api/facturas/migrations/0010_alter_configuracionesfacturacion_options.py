# Generated by Django 4.1.3 on 2023-01-31 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0009_alter_facturas_fecha_expedicion_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configuracionesfacturacion',
            options={'get_latest_by': 'created', 'managed': True, 'ordering': ['-created', '-updated'], 'verbose_name': 'configuraciones_facturacion', 'verbose_name_plural': 'configuraciones facturacion'},
        ),
    ]
