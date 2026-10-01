"""
Celery application for saleswithai (placeholder).
Kept for compatibility with existing generate_email / users apps.
The passes app does NOT use Celery — all work runs synchronously.
"""
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleswithai.settings")

app = Celery("saleswithai")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
