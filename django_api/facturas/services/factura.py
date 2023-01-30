import requests
import json
import random

# Date
from datetime import timedelta

# Django
from django.utils import timezone
from django.db.models import Sum

# Models
from ..models.facturas import Facturas, DetalleFactura
from django_api.contratos.models.contratos import Contratos
from django_api.servicios.models.servicios import Servicios


class FacturaServices:

    DIAS_VENCIMIENTO = 10
    PORCENTAJE_RECARGO = 2

    def crear_factura(self, contrato_id):
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
        valor_pendiente_pago = self.get_valor_pendiente_pago_facturas(contrato)
        data = {
            'contrato': contrato,
            'fecha_expedicion': hoy,
            'fecha_vencimiento': fecha_vencimiento,
            'estado': Facturas.EstadoChoices.PENDIENTE,
            'numero_pago_electronico': self.__get_numero_pago_electronico(),
            'valor_pendiente_pago': valor_pendiente_pago,
            'is_recargo': (True if valor_pendiente_pago > 0 else False)
        }
        return Facturas.objects.create(**data)

    def __crear_detalle_factura(self, contrato: Contratos, factura: Facturas, servicio: Servicios):
        lectura_anterior = self.get_lectura_anterior_servicio(contrato, factura, servicio)
        lectura_actual = self.get_lectura_actual_servicio(contrato)
        consumo_actual = (lectura_actual - lectura_anterior)
        valor_unitario = servicio.valor_unitario
        valor_total = (consumo_actual * valor_unitario)
        valor_recargo = self.get_valor_recargo_servicio(contrato, factura, servicio)
        total_a_pagar = (valor_total + valor_recargo)

        data = {
            'factura_id': factura.id,
            'servicio': servicio.id,
            'lectura_anterior': lectura_anterior,
            'lectura_actual': lectura_actual,
            'consumo_actual': consumo_actual,
            'valor_unitario': valor_unitario,
            'valor_total': valor_total,
            'porcentaje_recargo': servicio.porcentaje_recargo_mora,
            'valor_recargo': valor_recargo,
            'total_a_pagar': total_a_pagar
        }
        
        return DetalleFactura.objects.create(**data)

    def __get_numero_pago_electronico(self):
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
            deuda=Sum('total_a_pagar')
        )
        valor = facturas_pendientes_pago[0]['deuda']

        print('** get_valor_pendiente_pago_facturas: ', facturas_pendientes_pago.query)
        print('** valor: ', valor)

        return valor

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
            'servisio_id'
        ).annotate(
            deuda=Sum('total_a_pagar')
        ).exclude(
            factura_id=factura.id
        )
        valor = detalles_pendientes_pago[0]['deuda']

        print('** get_valor_pendiente_pago_servicio: ', detalles_pendientes_pago.query)
        print('** valor: ', valor)

        return valor

    def get_detalle_anterior_servicio(self, contrato: Contratos, factura: Facturas, servicio: Servicios):
        detalle = DetalleFactura.objects.filter(
            factura__contrato_id=contrato.id,
            servicio_id=servicio.id,
        ).exclude(
            factura_id=factura.id,
            factura__estado=Facturas.EstadoChoices.INACTIVA
        ).order_by('factura_id').first()

        print('** get_detalle_anterior_servicio: ', detalle.query)

        return detalle

    def get_lectura_anterior_servicio(self, contrato: Contratos, factura: Facturas, servicio: Servicios):
        detalle_anterior = self.get_detalle_anterior_servicio(contrato, factura, servicio)
        if detalle_anterior is None:
            return 0
        else:
            return detalle_anterior.lectura_actual

    def get_lectura_actual_servicio(self, contrato: Contratos):
        url = "https://energy-service-ds-v3cot.ondigitalocean.app/consumption"
        payload = json.dumps({
            "client_id": contrato.cliente.identification_number
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)
        data = json.loads(response.text)
        print('*** get_lectura_actual_servicio: ', data)
        return data['energy consumption']