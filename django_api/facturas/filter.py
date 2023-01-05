
# Django
from django_filters.rest_framework import BaseInFilter, NumberFilter, DateFilter
import rest_framework_filters as filters

# Models
from .models.facturas import Facturas


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