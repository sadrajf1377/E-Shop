from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','foroush_gah_postgresql.settings')

app=Celery('foroush_gah_postgresql')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()