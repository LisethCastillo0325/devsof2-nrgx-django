import os

from celery import Celery

from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('django_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'verificar-facturacion-servicios-cada-dia': {
        'task': 'facturacion_servicios',
        'schedule': crontab(minute=0, hour=6),
        'args': ()
    },
}

app.conf.timezone = 'America/Bogota'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')