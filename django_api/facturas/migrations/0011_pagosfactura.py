# Generated by Django 4.1.3 on 2023-04-14 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bancos', '0001_initial'),
        ('facturas', '0010_alter_configuracionesfacturacion_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagosFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Fecha en la cual fue creado.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Fecha en la que fue actualizdo por últimavez.', verbose_name='updated at')),
                ('forma_pago', models.CharField(choices=[('1', 'PRESECIAL'), ('2', 'BANCO'), ('3', 'VIRTUAL')], max_length=1, verbose_name='Forma de pago')),
                ('total_pago', models.FloatField(verbose_name='Total de pago')),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bancos.bancos')),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturas.facturas')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'pagos_factura',
                'verbose_name_plural': 'pagos de facturas',
                'db_table': 'pagos_factura',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
    ]