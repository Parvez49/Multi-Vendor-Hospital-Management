from celery import shared_task
from datetime import datetime, timedelta


from Accounts.models import Notification
from .models import DoctorAppointment


@shared_task
def send_appointment_reminders():
    current_time = datetime.now()

    # Calculate the time 15 minutes from now
    notification_time = current_time + timedelta(minutes=15) + timedelta(hours=6)

    # Get upcoming appointments within 15 minutes of the scheduled time
    upcoming_appointments = DoctorAppointment.objects.filter(
        date=notification_time.date(),
        doctor_schedule_day__doctor_schedule__start_time__lte=notification_time.time(),
        doctor_schedule_day__doctor_schedule__end_time__gte=notification_time.time(),
        isnotified=False,
    )

    print("upcoming_appointments", upcoming_appointments)

    for appointment in upcoming_appointments:
        # send a gmail to patient

        notification_head = "Upcoming Appointment Reminder"
        content = f"Your appointment is scheduled for {appointment.date} at {appointment.doctor_schedule_day.doctor_schedule.start_time}."

        patient_data = {
            "recipient": appointment.patient,
            "notification_head": notification_head,
            "content": content,
        }
        Notification.objects.create(**patient_data)
        appointment.isnotified = True
        appointment.save()
