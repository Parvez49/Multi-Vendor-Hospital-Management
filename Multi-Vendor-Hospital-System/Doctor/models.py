from django.db import models

from autoslug import AutoSlugField


from Accounts.models import User
from Hospital.models import Hospital
from datetime import date, time
from Common.models import BaseModelWithUID


from Common.models import Days, Specialty


class Doctor(BaseModelWithUID):
    doctor_info = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_full_name(self):
        return self.doctor_info.get_full_name()

    slug = AutoSlugField(populate_from="get_full_name", unique=True)
    # The department within the hospital (e.g., Cardiology, Pediatrics) where the doctor works.
    department = models.CharField(max_length=100)
    # The doctor's designation or title within the hospital (e.g., Cardiologist, Surgeon).
    designation = models.CharField(max_length=100)
    #  field can store information about the doctor's academic degrees (e.g., MBBS, MD, PhD).
    degrees = models.CharField(max_length=255)
    # The name of the medical school where the doctor received their degree.
    medical_school = models.CharField(max_length=255)
    # The doctor's medical license number.
    license_number = models.CharField(max_length=50)
    # The expiration date of the medical license.
    license_expiry_date = models.DateField()
    emergency_contact = models.CharField(max_length=15)
    # Details about the doctor's residency, if applicable.

    languages_spoken = models.TextField()
    # specialties = models.ManyToManyField('Specialty') # such as cardiology, pediatrics, orthopedics, etc.
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.doctor_info.first_name


class DoctorSpecialtyConnector(BaseModelWithUID):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)


ACTIVITY_CHOICES = (
    ("patient_exam", "Patient Examination"),
    ("surgery", "Surgery"),
    ("testing_lab", "Testing Lab"),
)


class DoctorSchedule(BaseModelWithUID):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    # days_of_week = models.ManyToManyField('Days') # or we can use string "saturday sunday monday"
    start_time = models.TimeField(
        default=time(9, 0)
    )  # Default start time, e.g., 9:00 AM
    end_time = models.TimeField(default=time(17, 0))  # Default end time, e.g., 5:00 PM
    activity_type = models.CharField(
        max_length=20, choices=ACTIVITY_CHOICES, default="patient_exam"
    )
    maximum_patient = models.IntegerField()

    def __str__(self):
        return f"{self.doctor.doctor_info.first_name} {self.hospital.hospital_name}"


class DoctorScheduleDaysConnector(BaseModelWithUID):
    doctor_schedule = models.ForeignKey(DoctorSchedule, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Doctor:{self.doctor_schedule.doctor.doctor_info.first_name} Hospital:{self.doctor_schedule.hospital.hospital_name} Day:{self.day}"


class EmergencyDoctorScedule(BaseModelWithUID):
    doctor_schedule = models.ForeignKey(DoctorSchedule, on_delete=models.CASCADE)
    schedule_date = models.DateField(blank=True)

    def __str__(self):
        return f"{self.doctor_schedule.doctor.doctor_info.first_name} {self.doctor_schedule.hospital.hospital_name} {self.schedule_date}"
