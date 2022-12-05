# Comandos Docker

Construir contenedor

    docker build -t devsof/django-app -f compose/local/django/Dockerfile .

Correr contenedor

    docker run -v /home/liseth/Documentos/desarrollo/proyectos/dessoft-1/django_api/django_api/:/app --env-file=./.envs/.local/.django --env-file=./.envs/.local/.postgres -p 8000:8000 devsof/django-app /start


# Comandos Docker Compose

### En el ambiente Local

Construir proyecto

    docker-compose build

Ejecutar proyecto

    docker-compose up

Crear super usuario

    docker-compose run --rm django python manage.py createsuperuser

# Entornos virtuales

Crear entorno vitual

```
virtualenv django_api
source django_api/bin/activate
```

Verificar librerias

    pip freeze

Migrar librerías a un archivo

    pip freeze > requirements.txt

Instalar librerías desde un archivo

    pip install -r requirements.txt
