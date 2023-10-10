from django.core.management.base import BaseCommand

from Accounts.models import User
from Common.models import Days, Specialty
from Doctor.models import (
    Doctor,
    DoctorSpecialtyConnector,
    DoctorSchedule,
    DoctorScheduleDaysConnector,
)
from Hospital.models import Hospital

from datetime import time


class Command(BaseCommand):
    help = "List all Doctor Model data in the database"

    def handle(self, *args, **kwargs):
        """
        user, created = User.objects.get_or_create(
            email="doctor@gmail.com",
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
        user.set_password("doctor")
        user.save()
        # Create a doctor associated with the user
        doctor, created = Doctor.objects.get_or_create(
            doctor_info=user,
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
        if created:
            self.stdout.write(self.style.SUCCESS("Sample data inserted successfully"))
        else:
            self.stdout.write(self.style.WARNING("Sample data already exists"))

        """

        data = {
            "doctors": [
                {
                    "doctor_info": {
                        "email": "John@gmail.com",
                        "first_name": "Dr. John",
                        "last_name": "Smith",
                        "gender": "Male",
                        "date_of_birth": "1975-03-12",
                        "height": 180.0,
                        "weight": 78,
                        "blood_group": "A+",
                        "nationality": "American",
                        "contact_number": "+134567890",
                    },
                    "department": "Cardiology",
                    "designation": "Cardiologist",
                    "degrees": "MD, PhD",
                    "medical_school": "Harvard Medical School",
                    "license_number": "MD123456",
                    "license_expiry_date": "2030-12-31",
                    "emergency_contact": "+123567901",
                    "languages_spoken": "English, Spanish",
                    "notes": "Specializes in heart diseases and cardiac care.",
                },
                {
                    "doctor_info": {
                        "email": "Johnson@gmail.com",
                        "first_name": "Dr. Alice",
                        "last_name": "Johnson",
                        "gender": "Female",
                        "date_of_birth": "1980-05-22",
                        "height": 165.5,
                        "weight": 60,
                        "blood_group": "B-",
                        "nationality": "British",
                        "contact_number": "+440712567",
                    },
                    "department": "Pediatrics",
                    "designation": "Pediatrician",
                    "degrees": "MBBS, DCH",
                    "medical_school": "University College London Medical School",
                    "license_number": "MBBS7890",
                    "license_expiry_date": "2032-06-30",
                    "emergency_contact": "+442098432",
                    "languages_spoken": "English, French",
                    "notes": "Specializes in child healthcare and development.",
                },
                {
                    "doctor_info": {
                        "email": "david@gmail.com",
                        "first_name": "Dr. David",
                        "last_name": "Brown",
                        "gender": "Male",
                        "date_of_birth": "1978-08-10",
                        "height": 175.0,
                        "weight": 75,
                        "blood_group": "O+",
                        "nationality": "Canadian",
                        "contact_number": "+1655234",
                    },
                    "department": "Orthopedics",
                    "designation": "Orthopedic Surgeon",
                    "degrees": "MD, FRCS",
                    "medical_school": "University of Toronto Faculty of Medicine",
                    "license_number": "MD456789",
                    "license_expiry_date": "2031-11-15",
                    "emergency_contact": "+1604237",
                    "languages_spoken": "English",
                    "notes": "Specializes in orthopedic surgery and joint replacements.",
                },
                {
                    "doctor_info": {
                        "email": "emily@gmail.com",
                        "first_name": "Dr. Emily",
                        "last_name": "Lee",
                        "gender": "Female",
                        "date_of_birth": "1982-12-05",
                        "height": 168.0,
                        "weight": 62,
                        "blood_group": "AB+",
                        "nationality": "Australian",
                        "contact_number": "+61987432",
                    },
                    "department": "Dermatology",
                    "designation": "Dermatologist",
                    "degrees": "MBBS, MD",
                    "medical_school": "University of Sydney Medical School",
                    "license_number": "MBBS12345",
                    "license_expiry_date": "2033-03-20",
                    "emergency_contact": "+6223789",
                    "languages_spoken": "English",
                    "notes": "Specializes in skin disorders and cosmetic dermatology.",
                },
                {
                    "doctor_info": {
                        "email": "michael@gmail.com",
                        "first_name": "Dr. Michael",
                        "last_name": "Garcia",
                        "gender": "Male",
                        "date_of_birth": "1977-09-18",
                        "height": 178.5,
                        "weight": 80,
                        "blood_group": "A-",
                        "nationality": "Spanish",
                        "contact_number": "+34912356",
                    },
                    "department": "Neurology",
                    "designation": "Neurologist",
                    "degrees": "MD, PhD",
                    "medical_school": "University of Barcelona Faculty of Medicine",
                    "license_number": "MD7890123",
                    "license_expiry_date": "2034-07-31",
                    "emergency_contact": "+3417653",
                    "languages_spoken": "Spanish, English",
                    "notes": "Specializes in neurological disorders and brain health.",
                },
            ]
        }
        for dat in data["doctors"]:
            doctor_info = dat.pop("doctor_info")
            user, created = User.objects.get_or_create(**doctor_info)
            user.set_password("doctor")
            user.save()
            Doctor.objects.get_or_create(doctor_info=user, defaults=dat)
