from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from Accounts.models import Notification
from Hospital.models import Hospital

from .models import DoctorAppointment


@receiver(post_save, sender=Hospital)
@receiver(post_delete, sender=Hospital)
def invalidate_hospital_list_cache(sender, instance, **kwargs):
    cache.delete("hospital_list")


@receiver(post_save, sender=DoctorAppointment)
def notify_doctor_and_patient(sender, instance, created, **kwargs):
    if created:
        print("notification")
        # ------------ Notification ---------------
        patient_data = {
            "recipient": instance.patient,
            "notification_head": "Appointment Accepted",
            "content": f"Date: {instance.date} " + "More info",
        }
        Notification.objects.create(**patient_data)
        doctor_data = {
            "recipient": instance.doctor_schedule_day.doctor_schedule.doctor.doctor_info,
            "notification_head": "New Patient Schedule",
            "content": f"Date: {instance.date} " + "More info",
        }
        Notification.objects.create(**doctor_data)

        # ----------------- email send --------------------------
        doctor_email = (
            instance.doctor_schedule_day.doctor_schedule.doctor.doctor_info.email
        )
        print(doctor_email)
        # email_subject = "New Appoinment"
        # message = f"Patient Name: {instance.patient.first_name}\n"

        # # send_mail(email_subject, message, settings.EMAIL_HOST_USER, [doctor_email])

        # patient_email = instance.patient.email
        # email_subject = "Successfully created your appointment"
        # message = f"Patient Name: {instance.user_data.first_name}\n"
        # send_mail(email_subject, message, settings.EMAIL_HOST_USER, [patient_email])

        print("notify")
