# Generated by Django 4.1.3 on 2023-01-29 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0004_publicidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicidad',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Estado'),
        ),
    ]
