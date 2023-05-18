# Celery
from celery import shared_task
from django_api.facturas.services.factura import FacturaServices


@shared_task(name="facturacion_servicios")
def facturacion_servicios():
    service = FacturaServices()
    facturas = service.crear_facturas_contratos()

    return f"Se crearon {len(facturas)} facturas."