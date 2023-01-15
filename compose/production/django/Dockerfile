FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
  && apt -y install libnss3-dev libssl-dev libsqlite3-dev libreadline-dev \
  && apt -y install libffi-dev curl libbz2-dev \
  && apt -y install gcc \
  # && apt -y install python3.9-dev \
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

# Instalar librerias wkhtmltopdf
RUN apt-get update
RUN apt-get -f -y install wkhtmltopdf
RUN apt-get -y install zlib1g fontconfig libxrender1 libfreetype6 libxext6 libx11-6

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown django /start

COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown django /start-celeryworker

COPY ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown django /start-celerybeat

COPY ./compose/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
