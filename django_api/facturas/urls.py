"""Contratos urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from django_api.facturas import views

router = DefaultRouter()
router.register(r'facturas', views.FacturasViewSet, basename='facturas')
router.register(r'publicidad', views.PublicidadViewSet, basename='publicidad')
router.register(
    r'configuraciones_facturacion', 
    views.ConfiguracionesFacturacionViewSet, 
    basename='configuraciones_facturacion'
)
router.register(r'facturas/pagos', views.PagosFacturasViewSet, basename='facturas-pagos')

urlpatterns = [
    path('', include(router.urls)),
]
