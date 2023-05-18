from django.test import TestCase
from django_api.servicios.models import Servicios

class ServicioModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Servicios.objects.create(nombre='Servicio 1', valor_unitario=0.0)
        Servicios.objects.create(nombre='Servicio 2', valor_unitario=3.44)

    def test_nombre_label(self):
        servicio = Servicios.objects.get(id=1)
        field_label = servicio._meta.get_field('nombre').verbose_name.lower()
        self.assertEqual(field_label, 'nombre')

    def test_listar_servicios(self):
        servicios = Servicios.objects.all()
        self.assertEqual(servicios.count(), 2)

        servicio_1 = servicios[1]
        self.assertEqual(servicio_1.nombre, 'Servicio 1')
        self.assertEqual(servicio_1.valor_unitario, 0.0)

        servicio_2 = servicios[0]
        self.assertEqual(servicio_2.nombre, 'Servicio 2')
        self.assertEqual(servicio_2.valor_unitario, 3.44)

    def test_crear_servicio(self):
        servicio = Servicios.objects.create(nombre='Servicio 3', valor_unitario=0.0)
        self.assertEqual(servicio.id, 3)
        self.assertEqual(servicio.nombre, 'Servicio 3')


    def test_actualizar_servicio(self):
        servicio = Servicios.objects.get(id=1)
        servicio.nombre = 'Nuevo nombre de servicio'
        servicio.valor_unitario = 1.99
        servicio.save()

        servicio_actualizado = Servicios.objects.get(id=1)
        self.assertEqual(servicio_actualizado.nombre, 'Nuevo nombre de servicio')
        self.assertEqual(servicio_actualizado.valor_unitario, 1.99)
        