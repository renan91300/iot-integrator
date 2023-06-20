# celery.py
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cibele.settings')

app = Celery('cibele')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()