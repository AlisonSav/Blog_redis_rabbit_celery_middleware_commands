import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("worker")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
# app.conf.beat_schedule = {
#     "add-every-2-hour": {
#         "task": "bee.tasks.add_quote",
#         "schedule": crontab(hour="1-23/2"),
#     },
#     "add-every-15-seconds": {
#         "task": "mac.tasks.add",
#         "schedule": 15,
#         "args": (1, 5),
#     },
# }


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")  # noqa T201
