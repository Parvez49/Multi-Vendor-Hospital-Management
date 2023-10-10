import datetime
import jwt
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


@shared_task
def send_password_reset_email(email):
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(hours=1),  # Expiration after 1 hour
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, "secret", algorithm="HS256")
    reset_link = f"http://127.0.0.1:8000/accounts/password/reset/{token}"
    email_subject = "Password Reset"
    message = f"Click the link below to reset your password:\n{reset_link}"
    send_mail(email_subject, message, settings.EMAIL_HOST_USER, [email])


@shared_task
def send_verification_email(email):
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(hours=1),  # Expiration after 1 hour
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, "secret", algorithm="HS256")
    link = f"http://127.0.0.1:8000/accounts/verify/{token}"

    email_subject = "Account Verification - Multi-Vendor Hospital Management System"
    message = f"We are pleased to inform you that your account with Multi-Vendor Hospital has been successfully created. Before you can access your account and start using our services, we require you to verify your email address.\n{link}\n Please note that this verification link will expire in one hour from the time of this email. If you did not create an account with PHCloud Limited, or if you believe this email was sent to you in error, please disregard it. Your account will remain inactive. Thank you for choosing our system. We look forward to serving you. \n Sincerely, \n System Team"

    send_mail(email_subject, message, settings.EMAIL_HOST_USER, [email])
