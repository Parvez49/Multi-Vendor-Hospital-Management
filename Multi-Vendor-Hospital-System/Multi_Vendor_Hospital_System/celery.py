import os

from celery import Celery
from datetime import timedelta


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Multi_Vendor_Hospital_System.settings")

app = Celery("Multi_Vendor_Hospital_System")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

# Configure Celery Beat schedule for the task
app.conf.beat_schedule = {
    "send-appointment-reminders": {
        "task": "Patient.tasks.send_appointment_reminders",
        "schedule": timedelta(minutes=1),
    },
}


# celery -A Multi_Vendor_Medical_System worker --loglevel=info

# celery -A Multi_Vendor_Medical_System beat


# Celery Monitoring using Flower
# pip install flower
# celery -A Multi_Vendor_Medical_System flower --port=5555
# celery -A Multi_Vendor_Medical_System flower
#
