# Django REST Framework
from rest_framework import serializers


class UploadFileCsvExcelSerializer(serializers.Serializer):
    archivo = serializers.FileField()
    extension = serializers.ReadOnlyField()

    EXTENSION_EXCEL = ['xlsm', 'xlsx']
    EXTENSION_CSV = ['csv']

    def validate(self, data):

        archivo_split = data['archivo'].name.split('.')
        if len(archivo_split) <= 1:
            raise serializers.ValidationError({'detail': "Error obteniendo la extensión del archivo"})

        data['extension'] = str(archivo_split[len(archivo_split) - 1]).lower()
        extenciones_habilies = self.EXTENSION_EXCEL + self.EXTENSION_CSV

        if data['extension'] not in extenciones_habilies:
            raise serializers.ValidationError({
                'detail': "Archivo con extensión incorrecta, asegúrese "
                          "de que esté entre las siguientes: {}".format(", ".join(extenciones_habilies))})
        return data
