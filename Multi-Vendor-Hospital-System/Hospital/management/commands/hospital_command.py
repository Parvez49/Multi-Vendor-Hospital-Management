from django.core.management.base import BaseCommand

from Accounts.models import User
from Common.models import Days, Specialty, HospitalRole
from Doctor.models import (
    Doctor,
    DoctorSpecialtyConnector,
    DoctorSchedule,
    DoctorScheduleDaysConnector,
)
from Hospital.models import (
    Founder,
    Hospital,
    HospitalSpecialtyConnector,
    UserHospitalRole,
    UserHospitalRoleConnector,
)

from datetime import time


class Command(BaseCommand):
    help = "List all Doctor Model data in the database"

    def handle(self, *args, **kwargs):
        hospital, created = Hospital.objects.get_or_create(
            registration_no="12345",
            defaults={
                "hospital_name": "City Hospital",
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
        specialty, created = Specialty.objects.get_or_create(specialty="Cardiology")

        hospital_sp, created = HospitalSpecialtyConnector.objects.get_or_create(
            hospital=hospital, specialty=specialty
        )
        user, created = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "first_name": "Abul",
                "last_name": "Kalam",
                "gender": "Male",
                "date_of_birth": "1995-01-01",
                "height": 175.0,
                "weight": 70,
                "blood_group": "A+",
                "nationality": "BD",
                "contact_number": "+1234567890",
            },
        )
        user.set_password("admin")
        user.save()

        founder, created = Founder.objects.get_or_create(
            founder=user, hospital=hospital
        )
        user_hospital, created = UserHospitalRole.objects.get_or_create(
            user=user, hospital=hospital
        )
        role, created = HospitalRole.objects.get_or_create(role="Admin")

        user_hospital_role, created = UserHospitalRoleConnector.objects.get_or_create(
            hospital_user=user_hospital, role=role
        )

        user, created = User.objects.get_or_create(
            email="doctor@example.com",
            defaults={
                "first_name": "Istiaq",
                "last_name": "Ahmed",
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

        user_hospital, created = UserHospitalRole.objects.get_or_create(
            user=user, hospital=hospital
        )
        role, created = HospitalRole.objects.get_or_create(role="Doctor")

        user_hospital_role, created = UserHospitalRoleConnector.objects.get_or_create(
            hospital_user=user_hospital, role=role
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Sample data inserted successfully"))
        else:
            self.stdout.write(self.style.WARNING("Sample data already exists"))

        # hospital_data = {
        #     "hospitals": [
        #         {
        #             "registration_no": "DHK-HOSP-001",
        #             "hospital_name": "Dhaka General Hospital",
        #             "city": "Dhaka",
        #             "state": "Dhaka",
        #             "postal_code": "1205",
        #             "country": "Bangladesh",
        #             "contact_number": "+8809875432",
        #             "website": "http://www.dhakageneralhospital.com",
        #             "description": "Dhaka General Hospital is a leading healthcare facility in Dhaka, committed to providing high-quality medical services to the community.",
        #             "additional_notes": "We specialize in cardiology, orthopedics, and general surgery.",
        #             "operating_hours": "Monday to Saturday: 8:00 AM - 6:00 PM",
        #             "insurance_accepted": "We accept all major health insurance plans.",
        #             "facilities": "Parking, Cafeteria, Pharmacy, Laboratory, Radiology",
        #         },
        #         {
        #             "registration_no": "DHK-HOSP-002",
        #             "hospital_name": "Dhaka Children's Hospital",
        #             "city": "Dhaka",
        #             "state": "Dhaka",
        #             "postal_code": "1219",
        #             "country": "Bangladesh",
        #             "contact_number": "+8802456890",
        #             "website": "http://www.dhakachildrenshospital.com",
        #             "description": "Dhaka Children's Hospital is a dedicated pediatric hospital, providing comprehensive healthcare services for children.",
        #             "additional_notes": "We have a team of specialized pediatricians and child-friendly facilities.",
        #             "operating_hours": "Open 24/7",
        #             "insurance_accepted": "We accept most health insurance plans for children.",
        #             "facilities": "Pediatric ICU, Play Area, Child-Friendly Rooms",
        #         },
        #         {
        #             "registration_no": "DHK-HOSP-003",
        #             "hospital_name": "Dhaka Heart Center",
        #             "city": "Dhaka",
        #             "state": "Dhaka",
        #             "postal_code": "1208",
        #             "country": "Bangladesh",
        #             "contact_number": "+8802234678",
        #             "website": "http://www.dhakaheartcenter.com",
        #             "description": "Dhaka Heart Center is a specialized cardiac care center, known for its expertise in treating heart diseases.",
        #             "additional_notes": "Our cardiology department is equipped with the latest technology for heart diagnosis and treatment.",
        #             "operating_hours": "Monday to Sunday: 7:00 AM - 9:00 PM",
        #             "insurance_accepted": "We work with major health insurance providers for cardiac treatments.",
        #             "facilities": "Cardiac ICU, Cardiac Catheterization Lab, Heart Surgery Center",
        #         },
        #         {
        #             "registration_no": "DHK-HOSP-004",
        #             "hospital_name": "Dhaka OrthoCare Hospital",
        #             "city": "Dhaka",
        #             "state": "Dhaka",
        #             "postal_code": "1220",
        #             "country": "Bangladesh",
        #             "contact_number": "+8802346789",
        #             "website": "http://www.dhakaorthocarehospital.com",
        #             "description": "Dhaka OrthoCare Hospital specializes in orthopedic care and offers a range of services for musculoskeletal conditions.",
        #             "additional_notes": "Our team of orthopedic surgeons provides personalized care for patients with bone and joint issues.",
        #             "operating_hours": "Monday to Saturday: 9:00 AM - 7:00 PM",
        #             "insurance_accepted": "We accept health insurance for orthopedic treatments.",
        #             "facilities": "Orthopedic Surgery Center, Rehabilitation Center, Physical Therapy",
        #         },
        #         {
        #             "registration_no": "DHK-HOSP-005",
        #             "hospital_name": "Dhaka Women's Hospital",
        #             "city": "Dhaka",
        #             "state": "Dhaka",
        #             "postal_code": "1207",
        #             "country": "Bangladesh",
        #             "contact_number": "+8808765321",
        #             "website": "http://www.dhakawomenshospital.com",
        #             "description": "Dhaka Women's Hospital is dedicated to providing comprehensive healthcare services for women's health and wellness.",
        #             "additional_notes": "We have a team of experienced gynecologists and offer maternity and fertility services.",
        #             "operating_hours": "Monday to Saturday: 8:30 AM - 6:30 PM",
        #             "insurance_accepted": "We accept health insurance for women's healthcare services.",
        #             "facilities": "Maternity Ward, Gynecology Department, Fertility Clinic",
        #         },
        #     ]
        # }
        # for hos in hospital_data["hospitals"]:
        #     Hospital.objects.get_or_create(**hos)
