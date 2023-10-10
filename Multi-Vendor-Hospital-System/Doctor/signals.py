from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from Accounts.models import Notification
from .models import Doctor, DoctorScheduleDaysConnector, EmergencyDoctorScedule
import datetime


@receiver(post_save, sender=Doctor)
def notify_doctor(sender, instance, created, **kwargs):
    if created:
        # ------------ Notification ---------------
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        doctor_data = {
            "recipient": instance.doctor_info,
            "notification_head": f"Succesfully updated your doctor information",
            "content": f"Date: {formatted_datetime} " + "More info",
        }
        Notification.objects.create(**doctor_data)


@receiver(post_save, sender=DoctorScheduleDaysConnector)
def notify_doctor_day_schedule(sender, instance, created, **kwargs):
    if created:
        # ------------ Notification ---------------
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        doctor_data = {
            "recipient": instance.doctor_schedule.doctor.doctor_info,
            "notification_head": f"New schedule",
            "content": f"Date: {formatted_datetime} "
            + f"You have new schedule in {instance.doctor_schedule.hospital.hospital_name} and ....",
        }
        Notification.objects.create(**doctor_data)


@receiver(post_save, sender=EmergencyDoctorScedule)
def notify_doctor_date_schedule(sender, instance, created, **kwargs):
    if created:
        # ------------ Notification ---------------
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        doctor_data = {
            "recipient": instance.doctor_schedule.doctor.doctor_info,
            "notification_head": f"Emergency New Schedule",
            "content": f"Date: {formatted_datetime} "
            + f"You have new schedule in {instance.doctor_schedule.hospital.hospital_name} and ....",
        }
        Notification.objects.create(**doctor_data)
