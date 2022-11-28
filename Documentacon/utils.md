# crear entorno vitual

virtualenv django_api

source django_api/bin/activate

## verificar librerias

pip freeze

## migrar librerias

pip freeze > requirements.txt

## install desde archivo

pip install -r requirements.txt

# Comandos Docker

## construir contenedor

docker build -t devsof/django-app -f compose/local/django/Dockerfile .

## correr contenedor

docker run -v /home/liseth/Documentos/desarrollo/proyectos/dessoft-1/django_api/django_api/:/app --env-file=./.envs/.local/.django --env-file=./.envs/.local/.postgres -p 8000:8000 devsof/django-app /start

# Comandos Docker Compose

## En Local

### Construir proyecto

docker-compose build

### Ejecutar proyecto

docker-compose up

### Crear super usario

docker-compose run --rm django python manage.py createsuperuser
