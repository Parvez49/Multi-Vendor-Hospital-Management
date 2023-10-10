from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from Accounts.models import Notification
from .models import Founder, HospitalRole, UserHospitalRoleConnector
from .serializers import UserHospitalRoleConnectorSerializer
import datetime


@receiver(post_save, sender=UserHospitalRoleConnector)
def notify_assigned_role(sender, instance, created, **kwargs):
    if created:
        print("notification")
        # ------------ Notification ---------------
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Update the notification_head and content fields
        notification_head = f"Welcome! You are now assigned as a {instance.role} at {instance.hospital_user.hospital.hospital_name} Hospital"
        content = f"Date: {formatted_datetime}. You have been assigned a role at {instance.hospital_user.hospital.hospital_name} Hospital."

        founder_data = {
            "recipient": instance.hospital_user.user,
            "notification_head": notification_head,
            "content": content,
        }
        Notification.objects.create(**founder_data)


@receiver(post_save, sender=Founder)
def notify_founder_and_default_admin(sender, instance, created, **kwargs):
    if created:
        print("notification")
        # ------------ Notification ---------------

        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        hospital_name = instance.hospital.hospital_name

        notification_head = f"Welcome! You are a founder of {hospital_name} Hospital"
        content = (
            f"Date: {formatted_datetime}\n"
            f"Dear {instance.founder.first_name},\n"
            f"We are excited to welcome you as a founder of {hospital_name} Hospital.\n"
            f"You are also Admin of {hospital_name}\n"
            f"Thank you for your contribution to our organization.\n"
            f"For more information, please visit our website or contact us.\n"
        )

        founder_data = {
            "recipient": instance.founder,
            "notification_head": notification_head,
            "content": content,
        }
        Notification.objects.create(**founder_data)

        # # ----------------- Assinging default Role -------------------
        # admin_data = {
        #     "recipient": instance.founder,
        #     "notification_head": f"Admin of {instance.hospital.hospital_name}",
        #     "content": f"Date: {formatted_datetime} " + "More info",
        # }
        # Notification.objects.create(**admin_data)

        # ----------------- email send --------------------------

        # email_subject = "New Appoinment"
        # message = f"Patient Name: {instance.patient.first_name}\n"

        # # send_mail(email_subject, message, settings.EMAIL_HOST_USER, [doctor_email])

        # patient_email = instance.patient.email
        # email_subject = "Successfully created your appointment"
        # message = f"Patient Name: {instance.user_data.first_name}\n"
        # send_mail(email_subject, message, settings.EMAIL_HOST_USER, [patient_email])

        # print("notify")
