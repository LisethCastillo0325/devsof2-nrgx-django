# Generated by Django 4.1.3 on 2023-01-18 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detallefactura',
            options={'get_latest_by': 'created', 'managed': True, 'ordering': ['-created', '-updated'], 'verbose_name': 'detalle_factura', 'verbose_name_plural': 'detalles de factura'},
        ),
        migrations.AlterField(
            model_name='detallefactura',
            name='consumo_actual',
            field=models.IntegerField(verbose_name='Consumo actual'),
        ),
        migrations.AlterField(
            model_name='detallefactura',
            name='lectura_actual',
            field=models.BigIntegerField(verbose_name='Lectura actual'),
        ),
        migrations.AlterField(
            model_name='detallefactura',
            name='lectura_anterior',
            field=models.BigIntegerField(verbose_name='Lectura anterior'),
        ),
        migrations.AlterField(
            model_name='detallefactura',
            name='valor_total',
            field=models.FloatField(verbose_name='Valor total'),
        ),
        migrations.AlterField(
            model_name='detallefactura',
            name='valor_unitario',
            field=models.FloatField(verbose_name='Valor unitario'),
        ),
    ]
