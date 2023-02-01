
# Django
from django_filters.rest_framework import BaseInFilter, NumberFilter, DateFilter
import rest_framework_filters as filters

# Models
from .models.users import User


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class UsersFilter(filters.FilterSet):
    created__gte = DateFilter(field_name='created', lookup_expr='date__gte')
    created__lte = DateFilter(field_name='created', lookup_expr='date__lte')
    groups = NumberInFilter(field_name='groups', lookup_expr='in')

    class Meta:
        model = User
        fields = [
            'created__gte', 'created__lte', 'groups', 'created', 'is_active',
            'identification_type', 'identification_number', 'birth_date'
        ]