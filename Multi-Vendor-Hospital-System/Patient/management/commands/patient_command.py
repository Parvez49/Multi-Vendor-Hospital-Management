from django.core.management.base import BaseCommand

from Accounts.models import User
from Common.models import Days, Specialty, Medical_Test, Medicine
from Doctor.models import (
    Doctor,
    DoctorSpecialtyConnector,
    DoctorSchedule,
    DoctorScheduleDaysConnector,
)
from Hospital.models import Hospital
from Patient.models import (
    DoctorAppointment,
    Prescription,
    PrescriptionMedicalTestConnector,
    PrescriptionMedicineConnector,
)


from datetime import time


class Command(BaseCommand):
    help = "List all Doctor Model data in the database"

    def handle(self, *args, **kwargs):
        doctor_user, created = User.objects.get_or_create(
            email="doctor@example.com",
            defaults={
                "first_name": "first name 1",
                "last_name": "last name 1",
                "gender": "Male",
                "date_of_birth": "1995-01-01",
                "height": 175.0,
                "weight": 70,
                "blood_group": "A+",
                "nationality": "BD",
                "contact_number": "+1234567890",
            },
        )
        doctor.set_password("doctor")
        doctor.save()
        # Create a doctor associated with the user
        doctor, created = Doctor.objects.get_or_create(
            doctor_info=doctor_user,
            defaults={
                "department": "Cardiology",
                "designation": "Cardiologist",
                "degrees": "MBBS, MD",
                "medical_school": "Medical School",
                "license_number": "12345",
                "license_expiry_date": "2030-12-31",
                "emergency_contact": "+1234567890",
                "languages_spoken": "English,",
                "notes": "Sample notes",
            },
        )
        specialty, created = Specialty.objects.get_or_create(specialty="specialty 1")
        doctor_specialty, created = DoctorSpecialtyConnector.objects.get_or_create(
            doctor=doctor, specialty=specialty
        )
        hospital, created = Hospital.objects.get_or_create(
            registration_no="12345",
            defaults={
                "hospital_name": "Sample Hospital",
                "logo": "/home/Downloads/hospitallogo.png",
                "city": "Sample City",
                "state": "Sample State",
                "postal_code": "12345",
                "country": "Sample Country",
                "contact_number": "+1234567890",
                "website": "https://www.samplehospital.com",
                "description": "Sample description of the hospital",
                "additional_notes": "Additional notes about the hospital",
                "operating_hours": "9:00 AM - 5:00 PM",
                "insurance_accepted": "Sample insurance providers",
                "facilities": "Facility 1, Facility 2",
            },
        )

        start_time = time(9, 0)
        end_time = time(17, 0)
        doctor_schedule, created = DoctorSchedule.objects.get_or_create(
            doctor=doctor,
            hospital=hospital,
            start_time=start_time,
            end_time=end_time,
            activity_type="patient_exam",
            maximum_patient=10,
        )
        day, created = Days.objects.get_or_create(day="Monday")
        schedule_day, created = DoctorScheduleDaysConnector.objects.get_or_create(
            doctor_schedule=doctor_schedule, day=day
        )

        patient_user, created = User.objects.get_or_create(
            email="patient@example.com",
            defaults={
                "first_name": "first name 2",
                "last_name": "last name 2",
                "gender": "Male",
                "date_of_birth": "1995-01-01",
                "height": 175.0,
                "weight": 70,
                "blood_group": "A+",
                "nationality": "BD",
                "contact_number": "+123456567890",
            },
        )
        patient_user.set_password("patient")
        patient_user.save()
        doctor_appointment, created = DoctorAppointment.objects.get_or_create(
            doctor_schedule_day=schedule_day, patient=patient_user, date="2023-10-09"
        )

        prescription, created = Prescription.objects.get_or_create(
            patient_doctor_booking=doctor_appointment,
            defaults={
                "prescription_date": "2023-10-09",
                "previous_medications": "previous_medications",
                "diagnosis": "diagnosis",
                "special_instructions": "instructions",
            },
        )
        test, created = Medical_Test.objects.get_or_create(
            name="Test 1", defaults={"process": "process 1", "price": 450}
        )
        (
            prescription_test,
            created,
        ) = PrescriptionMedicalTestConnector.objects.get_or_create(
            prescription=prescription, test=test
        )
        medicine, created = Medicine.objects.get_or_create(
            name="Medicine 1",
            defaults={
                "dosage": "10mg",
                "duration": "7 days",
                "method_of_taken": "Orally",
                "morning": True,
                "noon": False,
                "evening": True,
                "price": 9.99,
            },
        )
        (
            prescription_medicine,
            created,
        ) = PrescriptionMedicineConnector.objects.get_or_create(
            prescription=prescription, medicine=medicine
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Sample data inserted successfully"))
        else:
            self.stdout.write(self.style.WARNING("Sample data already exists"))
