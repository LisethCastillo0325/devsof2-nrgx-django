# Generated by Django 4.1.3 on 2023-01-29 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0002_alter_servicios_porcentaje_recargo_mora'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicios',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Estado'),
        ),
    ]
