
# Django
from django_filters.rest_framework import BaseInFilter, NumberFilter, DateFilter
import rest_framework_filters as filters

# Models
from .models.facturas import Facturas
from .models.publicidad import Publicidad


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class FaturasFilter(filters.FilterSet):
    created__gte = DateFilter(field_name='created', lookup_expr='date__gte')
    created__lte = DateFilter(field_name='created', lookup_expr='date__lte')
    clientes = NumberInFilter(field_name='contrato__cliente', lookup_expr='in')
    contratos = NumberInFilter(field_name='contrato', lookup_expr='in')

    class Meta:
        model = Facturas
        fields = ['created__gte', 'created__lte', 'clientes', 'contratos']


class FaturasViewFilter(filters.FilterSet):
    created__gte = DateFilter(field_name='created', lookup_expr='date__gte')
    created__lte = DateFilter(field_name='created', lookup_expr='date__lte')
    contrato__cliente = NumberInFilter(field_name='contrato__cliente', lookup_expr='in')
    contrato = NumberInFilter(field_name='contrato', lookup_expr='in')
    fecha_expedicion = DateFilter(field_name='fecha_expedicion', lookup_expr='date')
    fecha_vencimiento = DateFilter(field_name='fecha_vencimiento', lookup_expr='date')

    class Meta:
        model = Facturas
        fields = (
            'contrato', 'contrato__cliente', 'contrato__cliente__identification_number',
            'estado', 'is_recargo', 'numero_pago_electronico', 'fecha_expedicion', 'fecha_vencimiento',
            'created__gte', 'created__lte'
        )


class PublicidadFilter(filters.FilterSet):
    fecha_vigencia_inicio = DateFilter(field_name='fecha_vigencia_inicio', lookup_expr='date__gte')
    fecha_vigencia_fin = DateFilter(field_name='fecha_vigencia_fin', lookup_expr='date__lte')

    class Meta:
        model = Publicidad
        fields = ['fecha_vigencia_inicio', 'fecha_vigencia_fin', 'seccion_factura', 'is_active']