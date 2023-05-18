from django_api.facturas.services.factura import FacturaServices


def test_longitud_numero_pago_electronico():
    service = FacturaServices()
    numero_pago = service.get_numero_pago_electronico()
    
    assert len(str(numero_pago)) == 15
