FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1

ENV XDG_RUNTIME_DIR=/tmp

RUN apt-get update \
    # dependencies for building Python packages
    && apt -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
    && apt -y install libnss3-dev libssl-dev libsqlite3-dev libreadline-dev \
    && apt -y install libffi-dev curl libbz2-dev \
    && apt -y install gcc \
    && apt-get install -y build-essential \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    # Librerias para xmlsec
    && apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl \
    # GCC
    && apt-get install -y manpages-dev \
    #
    && apt-get install -y xvfb python3-dev \
    && apt-get install -y python3 python-dev libffi-dev \
    && apt-get install -y libxslt1-dev zlib1g-dev \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

# Instalar librerias wkhtmltopdf
RUN apt-get update
RUN apt-get -f -y install wkhtmltopdf
RUN apt-get -y install zlib1g fontconfig libxrender1 libfreetype6 libxext6 libx11-6

WORKDIR /app

# Copiar el código fuente de la aplicación
COPY . .

ENTRYPOINT ["/entrypoint"]
