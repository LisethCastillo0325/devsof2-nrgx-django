"""Users urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from django_api.reportes import views

router = DefaultRouter()
router.register(r'reportes/clientes', views.ReportesClientesViewSet, basename='reporte_clientes')

urlpatterns = [
    path('', include(router.urls)),
]
