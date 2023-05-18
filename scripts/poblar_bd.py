from django.core.management import call_command


def poblar_datos_bd():
    call_command('loaddata', 'fixtures/departamentos.json')
    call_command('loaddata', 'fixtures/ciudades.json')
    call_command('loaddata', 'fixtures/roles.json')
    call_command('loaddata', 'fixtures/servicios.json')
    call_command('loaddata', 'fixtures/configuraciones_facturacion.json')
    call_command('loaddata', 'fixtures/bancos.json')

def run():
    print(">>> Inició creacion de datos en la BD...")
    poblar_datos_bd()
    print(">>> Finalizó creación de datos en la BD.")
