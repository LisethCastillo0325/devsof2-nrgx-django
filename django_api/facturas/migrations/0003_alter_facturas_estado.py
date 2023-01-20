# Generated by Django 4.1.3 on 2023-01-20 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0002_alter_detallefactura_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturas',
            name='estado',
            field=models.CharField(choices=[('1', 'PAGADA'), ('2', 'PENDIENTE'), ('3', 'INACTIVA')], default='2', max_length=1),
        ),
    ]
