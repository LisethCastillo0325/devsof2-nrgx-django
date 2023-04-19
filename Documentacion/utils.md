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

Crear migraciones

    docker-compose run --rm django python manage.py makemigrations

    docker-compose run --rm django python manage.py migrate

#### Ejecutar con base de datos local

Construir proyecto

    docker-compose -f local-db.yml build

Crear migraciones

    docker-compose -f local-db.yml run --rm django python manage.py makemigrations

    docker-compose -f local-db.yml run --rm django python manage.py migrate

Crear super usuario

    docker-compose -f local-db.yml run --rm django python manage.py createsuperuser

Crear datos iniciales en BD
    
    docker-compose -f local-db.yml run --rm django python manage.py runscript poblar_bd

Ejecutar proyecto

    docker-compose -f local-db.yml up


### En el ambiente Producción

Copiar o actualizar archivos estaticos

docker-compose -f local-db-production.yml run --rm django python manage.py collectstatic

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
