from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

from datetime import datetime

from Accounts.models import User
from Common.models import Days
from Doctor.models import Doctor, DoctorSchedule, DoctorScheduleDaysConnector
from Hospital.models import (
    Hospital,
    HospitalRole,
    UserHospitalRole,
    UserHospitalRoleConnector,
)

from .models import DoctorAppointment
from .serializers import (
    DoctorAppointmentSerializer,
    DoctorAppointmentUpdateDeleteSerializer,
)


class PatientDoctorAppointmentTestCase(APITestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user(
            email="patient@example.com",
            contact_number="+1234567",
            password="patientpassword",
        )
        self.hospital = Hospital.objects.create(
            registration_no="123456",
            hospital_name="Hospital 1",
            city="City 1",
            state="State 1",
            postal_code="12345",
            country="Country 1",
            contact_number="1234567890",
            operating_hours="8:00 AM - 5:00 PM",
            description="Description 1",
            additional_notes="Additional Notes 1",
            facilities="Facilities 1",
        )
        self.doctor_user = User.objects.create_user(
            email="doctor@example.com",
            contact_number="+4567890",
            password="doctorpassword",
        )
        self.doctor = Doctor.objects.create(
            doctor_info=self.doctor_user,
            department="Cardiology",
            designation="Cardiologist",
            degrees="MBBS, MD",
            medical_school="Medical School",
            license_number="12345",
            license_expiry_date="2023-12-31",
            emergency_contact="1234567890",
            languages_spoken="English, Spanish",
        )
        self.days = Days.objects.create(day="Monday")
        self.doctor_schedule = DoctorSchedule.objects.create(
            doctor=self.doctor,
            hospital=self.hospital,
            start_time="09:00:00",
            end_time="17:00:00",
            activity_type="patient_exam",
            maximum_patient=10,
        )
        self.connector = DoctorScheduleDaysConnector.objects.create(
            doctor_schedule=self.doctor_schedule,
            day=self.days,
        )
        self.appointment = DoctorAppointment.objects.create(
            doctor_schedule_day=self.connector,
            patient=self.patient_user,
            date="2023-10-02",
        )

        self.hospital_admin = User.objects.create_user(
            email="admin@example.com",
            contact_number="+324567890",
            password="adminpassword",
        )
        self.role = HospitalRole.objects.create(role="Admin")
        self.hospital_user = UserHospitalRole.objects.create(
            hospital=self.hospital, user=self.hospital_admin
        )
        self.user_role = UserHospitalRoleConnector.objects.create(
            hospital_user=self.hospital_user, role=self.role
        )
        self.client = APIClient()

    def test_list_patient_appointments_as_authenticated_user(self):
        self.client.force_authenticate(user=self.patient_user)
        url = reverse("patient-doctor-appointment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        serialized_appointment = DoctorAppointmentSerializer(self.appointment).data
        self.assertIn(serialized_appointment, data)

    def test_create_patient_appointment_as_authenticated_user(self):
        self.client.force_authenticate(user=self.patient_user)
        data = {
            "doctor_schedule_day": self.connector.uuid,
            "date": "2023-10-09",
        }
        url = reverse("patient-doctor-appointment-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DoctorAppointment.objects.count(), 2)
        created_appointment = DoctorAppointment.objects.latest("created_at")
        self.assertEqual(created_appointment.doctor_schedule_day, self.connector)
        self.assertEqual(created_appointment.patient, self.patient_user)
        self.assertEqual(str(created_appointment.date), "2023-10-09")

    def test_retrieve_update_delete_patient_appointment_as_authenticated_user(self):
        self.client.force_authenticate(user=self.hospital_admin)
        url = reverse(
            "patient-doctor-booking-detail",
            kwargs={
                "hospital_uuid": self.hospital.uuid,
                "appointment_uuid": self.appointment.uuid,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        serialized_appointment = DoctorAppointmentUpdateDeleteSerializer(
            self.appointment
        ).data
        self.assertEqual(data, serialized_appointment)
        updated_data = {
            "doctor_schedule_day": self.connector.uuid,
            "patient": self.patient_user.uuid,
            "date": "2023-10-16",
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_appointment = DoctorAppointment.objects.get(uuid=self.appointment.uuid)
        self.assertEqual(
            updated_appointment.date,
            datetime.strptime(updated_data["date"], "%Y-%m-%d").date(),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            DoctorAppointment.objects.filter(uuid=self.appointment.uuid).exists()
        )
