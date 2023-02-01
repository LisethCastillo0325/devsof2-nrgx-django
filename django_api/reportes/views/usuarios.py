# Django
from django.http import HttpResponse
from django.db.models.functions import Concat
from django.db.models import Value, F, Case, When, OuterRef, Subquery
from django.contrib.postgres.aggregates import StringAgg

# Django rest framework
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Utils
import io
import pandas
from django_pandas.io import read_frame
from django_api.utils.utils.utils import size_column_excel

from django_api.users.models import User

# Filter
from django_api.users.filter import UsersFilter

# Permisos
from rest_framework.permissions import IsAuthenticated


class ReporteUsuariosViewSet(GenericViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def registrados(self, request, **kwargs):

        """ Reporte Usuarios Regsitrados
            
            Reporte de usuarios registrados en el sistema
        """

        sq_rol_usuario = User.objects.values('groups__name').annotate(
            list_rol=StringAgg('groups__name', delimiter=', ')
        ).filter(id=OuterRef('id'))

        x = User.objects.annotate(
            nombre_completo=Concat('first_name', Value(' '), 'last_name'),
            celular=F('phone_number'),
            numero_identificacion=F('identification_number'),
            tipo_identificacion=Case(
                When(identification_type=User.IdentificationTypeChoices.CC, then=Value('CC')),
                When(identification_type=User.IdentificationTypeChoices.CE, then=Value('CE')),
                When(identification_type=User.IdentificationTypeChoices.NIT, then=Value('NIT')),
                default=Value('')
            ),
            fecha_nacimiento=F('birth_date'),
            estado=Case(
                When(is_active=False, then=Value('INACTIVO')),
                When(is_active=True, then=Value('ACTIVO')),
                default=Value('ACTIVO')
            ),
            roles=Subquery(sq_rol_usuario.values('list_rol')),
        )

        data = UsersFilter(request.GET, queryset=x)
        sio = io.BytesIO()
        reporte_usuarios = read_frame(data.qs)

        reporte_usuarios = self.adicionar_fecha_hora(
            reporte_usuarios, 'created', 'creacion')

        reporte_usuarios = reporte_usuarios[
            [
                "id", "nombre_completo",  "numero_identificacion", "tipo_identificacion", 
                "email", "celular", "fecha_nacimiento", 
                "estado", "roles", "fecha_creacion", "hora_creacion"
            ]
        ]

        datos_archivo = pandas.ExcelWriter(sio, engine='xlsxwriter')
        reporte_usuarios.to_excel(datos_archivo, sheet_name='reporte_usuarios', index=False)
        size_column_excel(datos_archivo, reporte_usuarios, 'reporte_usuarios')
        datos_archivo.save()

        sio.seek(0)
        workbook = sio.getvalue()
        response = HttpResponse(workbook, content_type="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=reporte_usuarios.xlsx'

        return response

    def adicionar_fecha_hora(self, reporte, nombre_campo, nombre_fecha):
        reporte[nombre_campo] = pandas.to_datetime(reporte[nombre_campo], format='%Y-%m-%d %H:%M:%S')
        fecha = {f'fecha_{nombre_fecha}': reporte[nombre_campo].dt.strftime('%d/%m/%Y')}
        hora = {f'hora_{nombre_fecha}': reporte[nombre_campo].dt.strftime('%H:%M')}
        reporte = reporte.assign(**fecha)
        reporte = reporte.assign(**hora)
        return reporte