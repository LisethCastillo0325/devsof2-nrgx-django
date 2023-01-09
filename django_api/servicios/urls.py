"""Servicios urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter


# Views
from django_api.servicios import views

router = DefaultRouter()
router.register(r'servicios', views.ServicioViewSet, basename='servicio')

