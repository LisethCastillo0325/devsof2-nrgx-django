

"""Contratos urls."""

"""
Este código define las URL de la aplicación "Contratos".

Se importa la función path de django.urls y la clase DefaultRouter de rest_framework.routers. Se importan
 también las vistas de la aplicación views que se utilizarán en las URL.

Se crea una instancia del enrutador DefaultRouter y se registra la vista ContratosViewSet utilizando el 
método register(). El primer parámetro de register() es el nombre de la URL que se utilizará para acceder
 a la vista, y el segundo parámetro es la vista en sí misma. En este caso, el nombre de la URL es 
 "contratos" y la vista es ContratosViewSet.

Finalmente, se define una lista de URL llamada urlpatterns, que incluye las URLs generadas por el 
enrutador (router.urls) y una URL vacía que redirige a las URLs generadas. 

"""

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
