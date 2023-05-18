import requests
import json
import random
import math

# Date
from datetime import timedelta

# Django
from django.utils import timezone
from django.db.models import Sum, Count
from django.core import exceptions

# Models
from ..models.facturas import Facturas, DetalleFactura, ConfiguracionesFacturacion
from django_api.contratos.models.contratos import Contratos
from django_api.servicios.models.servicios import Servicios, LogConsumoServicios

# Utils
from django_api.utils.exceptions import CustomValidationAPIException


class FacturaServices:

    DIAS_VENCIMIENTO = 10

    def crear_facturas_contratos(self):
        # Consultar Contratos activos
        contratos = Contratos.objects.filter(
            estado=Contratos.EstadoChoices.ACTIVO
        ).values_list('id', flat=True)
        
        facturas = []
        # Crear factura por cada contrato
        for contrato_id in contratos:
            facturas.append(self.crear_factura(contrato_id))

        return facturas

    def crear_factura(self, contrato_id):
        
        # Validación de día de cortte
        self.__validacion_dia_de_corte()

        valor_recargo = 0
        total_a_pagar = 0
        
        # Consultar Contrato
        contrato = Contratos.objects.select_related('cliente').get(id=contrato_id)

        # Crear encabezado factura
        factura = self.__crear_cabecera_factura(contrato)

        # Crear detalles de factura
        servicios = contrato.servicios.all()
        for servicio in servicios:
            detalle = self.__crear_detalle_factura(contrato, factura, servicio)
            valor_recargo += detalle.valor_recargo
            total_a_pagar += detalle.total_a_pagar

        # Actualizar totales factura
        factura.valor_recargo = valor_recargo
        factura.total_a_pagar = total_a_pagar
        factura.save()

        return factura

    def __crear_cabecera_factura(self, contrato: Contratos):
        hoy = timezone.now()
        fecha_vencimiento = hoy + timedelta(days=self.DIAS_VENCIMIENTO)
        valor_pendiente_pago, cantidad_facturas = self.get_valor_pendiente_pago_facturas(contrato)
        data = {
            'contrato': contrato,
            'fecha_expedicion': hoy,
            'fecha_vencimiento': fecha_vencimiento,
            'estado': Facturas.EstadoChoices.PENDIENTE,
            'numero_pago_electronico': self.get_numero_pago_electronico(),
            'valor_pendiente_pago': valor_pendiente_pago,
            'is_recargo': (True if cantidad_facturas >= 2 else False)
        }

        return Facturas.objects.create(**data)

    def __crear_detalle_factura(self, contrato: Contratos, factura: Facturas, servicio: Servicios):
        lectura_anterior = self.get_lectura_anterior_servicio(contrato, factura, servicio)
        lectura_actual = (lectura_anterior + self.get_lectura_actual_servicio(factura, servicio))
        consumo_actual = (lectura_actual - lectura_anterior)
        valor_unitario = servicio.valor_unitario
        valor_total = (consumo_actual * valor_unitario)
        valor_recargo = self.get_valor_recargo_servicio(contrato, factura, servicio)
        total_a_pagar = (valor_total + valor_recargo)

        data = {
            'factura_id': factura.id,
            'servicio_id': servicio.id,
            'lectura_anterior': lectura_anterior,
            'lectura_actual': lectura_actual,
            'consumo_actual': consumo_actual,
            'valor_unitario': valor_unitario,
            'valor_total': valor_total,
            'porcentaje_recargo': (0 if not factura.is_recargo else servicio.porcentaje_recargo_mora),
            'valor_recargo': valor_recargo,
            'total_a_pagar': total_a_pagar
        }
        
        return DetalleFactura.objects.create(**data)

    def get_numero_pago_electronico(self):
        numeros = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        # Barajar números
        random.shuffle(numeros)
        seleccionados = [str(random.choice(numeros)) for i in range(15)]
        return ''.join(seleccionados)

    def get_valor_pendiente_pago_facturas(self, contrato: Contratos):
        facturas_pendientes_pago = Facturas.objects.filter(
            estado=Facturas.EstadoChoices.PENDIENTE,
            contrato_id=contrato.id,
        ).values(
            'contrato_id'
        ).annotate(
            deuda=Sum('total_a_pagar'),
            cantidad_facturas=Count('id')
        )

        if facturas_pendientes_pago.count() == 0:
            valor = 0
            cantidad_facturas = 0
        else:
            valor = facturas_pendientes_pago[0]['deuda']
            cantidad_facturas = facturas_pendientes_pago[0]['cantidad_facturas']

        return valor, cantidad_facturas

    def get_valor_recargo_servicio(self, contrato: Contratos, factura: Facturas, servicio: Servicios):
        valor_recargo = 0
        if factura.is_recargo:
            porcentaje_recargo = servicio.porcentaje_recargo_mora
            valor_pendiente = self.get_valor_pendiente_pago_servicio(contrato, factura, servicio)
            valor_recargo = (valor_pendiente * porcentaje_recargo) / 100
        return valor_recargo

    def get_valor_pendiente_pago_servicio(self, contrato: Contratos, factura: Facturas, servicio: Servicios):
        detalles_pendientes_pago = DetalleFactura.objects.filter(
            factura__estado=Facturas.EstadoChoices.PENDIENTE,
            factura__contrato_id=contrato.id,
            servicio_id=servicio.id,
        ).values(
            'servicio_id'
        ).annotate(
            deuda=Sum('total_a_pagar')
        ).exclude(
            factura_id=factura.id
        )
        valor = detalles_pendientes_pago[0]['deuda']

        return valor

    def get_detalle_anterior_servicio(self, contrato: Contratos, factura: Facturas, servicio: Servicios):
        detalle = DetalleFactura.objects.filter(
            factura__contrato_id=contrato.id,
            servicio_id=servicio.id,
        ).exclude(
            factura_id=factura.id,
            factura__estado=Facturas.EstadoChoices.INACTIVA
        ).order_by('factura_id')
        
        return detalle.first()

    def get_lectura_anterior_servicio(self, contrato: Contratos, factura: Facturas, servicio: Servicios):
        detalle_anterior = self.get_detalle_anterior_servicio(contrato, factura, servicio)
        if detalle_anterior is None:
            return 0
        else:
            return detalle_anterior.lectura_actual

    def get_lectura_actual_servicio(self, factura: Facturas, servicio: Servicios):
        # url = "https://energy-service-ds-v3cot.ondigitalocean.app/consumption"
        # payload = json.dumps({
        #     "client_id": factura.contrato.cliente.identification_number
        # })
        # headers = {
        #     'Content-Type': 'application/json'
        # }
        # response = requests.post(url, headers=headers, json=payload)
        # data = json.loads(response.text)

        try:
            # lectura = data['energy consumption']
            lectura = random.randint(30, 150)
        except Exception:
            lectura = 0

        # # Log Consumo
        # self.__save_log_consumo_servicio(factura, servicio, lectura, payload, response)

        return lectura

    def __save_log_consumo_servicio(self, factura: Facturas, servicio: Servicios, lectura, payload, response):
        try:
            data_log = {
                'factura_id': factura.id,
                'servicio_id': servicio.id,
                'lectura': lectura,
                'data_sent': payload,
                'data_received': response.text
            }
            LogConsumoServicios.objects.create(**data_log)
        except Exception as error:
            print('*** Error en log consumo: ', error)

    def __validacion_dia_de_corte(self):
        configuracion = ConfiguracionesFacturacion.objects.order_by('id').values('dia_de_corte').first()
        if configuracion is None:
            raise CustomValidationAPIException({'detail': 'No existe configuración para la facturación.'})

        if configuracion['dia_de_corte'] is None:
            raise CustomValidationAPIException({'detail': 'No existe configuración de día de corte para la facturación.'})

        dia_hoy = timezone.now().day
        dia_de_corte = configuracion['dia_de_corte']

        if int(dia_hoy) != int(dia_de_corte):
            raise CustomValidationAPIException({
                'detail': f'El día de corte para la facturación es el día {dia_de_corte} de cada mes.'})