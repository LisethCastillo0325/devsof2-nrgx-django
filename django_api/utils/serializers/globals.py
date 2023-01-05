"""Global serializers."""

# Django REST Framework
from rest_framework import serializers


class DataChoiceSerializer(serializers.SerializerMethodField):
    """
    A read-only field that return the representation of a model field with choices.
    """

    def to_representation(self, value):
        # sample: 'get_XXXX_display'
        label = 'get_{field_name}_display'.format(field_name=self.field_name)
        value_choice = '{field_name}'.format(field_name=self.field_name)
        # retrieve instance method
        label = getattr(value, label)
        value_choice = getattr(value, value_choice)
        return {
            'value': value_choice,
            'label': label()
        }


class DataSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'value': instance.pk,
            'label': instance.nombre
        }