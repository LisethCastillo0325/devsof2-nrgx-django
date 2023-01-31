"""Contratos urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from django_api.contratos import views

router = DefaultRouter()
router.register(r'contratos', views.ContratosViewSet, basename='comntratos')

urlpatterns = [
    path('', include(router.urls)),
]
