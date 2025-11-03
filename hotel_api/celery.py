import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_api.settings")

app = Celery("hotel_api")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

