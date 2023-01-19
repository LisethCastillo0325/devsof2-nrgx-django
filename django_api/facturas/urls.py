"""Contratos urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from django_api.facturas import views

router = DefaultRouter()
router.register(r'facturas', views.FacturasViewSet, basename='facturas')

urlpatterns = [
    path('', include(router.urls)),
]
