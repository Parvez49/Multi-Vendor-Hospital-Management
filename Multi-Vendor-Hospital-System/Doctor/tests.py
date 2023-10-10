from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

from Accounts.models import User
from Common.models import Days, HospitalRole, Medical_Test, Medicine
from Hospital.models import Hospital, UserHospitalRole, UserHospitalRoleConnector
from Patient.models import (
    DoctorAppointment,
    Prescription,
    PrescriptionMedicalTestConnector,
    PrescriptionMedicineConnector,
)
from Patient.serializers import (
    PrescriptionSerializer,
    PrescriptionMedicalTestConnectorSerializer,
)

from .models import Doctor, DoctorSchedule, DoctorScheduleDaysConnector
from .serializers import (
    PrivateDoctorSerializer,
    PrivateDoctorScheduleDaysConnectorSerializer,
)


# ------------------------------------------


class DoctorAppointmentsPrescriptionTestCase(APITestCase):
    def setUp(self):
        self.doctor_user = User.objects.create_user(
            password="doctorpassword",
            email="doctor@example.com",
            contact_number="+123456",
        )
        self.patient_user = User.objects.create_user(
            password="patientpassword",
            email="patient@example.com",
            contact_number="+127899",
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
            date="2023-12-31",
        )
        self.prescription = Prescription.objects.create(
            patient_doctor_booking=self.appointment,
            previous_medications="Medication 1",
            diagnosis="Diagnosis 1",
            special_instructions="Instructions 1",
        )
        print(self.prescription.diagnosis)
        self.medical_test = Medical_Test.objects.create(
            name="Blood", process="process", price=450
        )
        self.medicine = Medicine.objects.create(
            name="Medicine 1",
            dosage="10mg",
            duration="7 days",
            method_of_taken="Orally",
            morning=True,
            noon=False,
            evening=True,
            price=9.99,
        )
        self.client = APIClient()

    def test_create_prescription_medical_test_connector_as_authenticated_user(self):
        self.client.force_authenticate(user=self.doctor_user)
        data = {"test": self.medical_test.uuid}
        url = reverse(
            "doctor-appointments-Prescription-medical-test",
            kwargs={
                "appointment_uuid": self.appointment.uuid,
                "prescription_uuid": self.prescription.uuid,
            },
        )
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrescriptionMedicalTestConnector.objects.count(), 1)
        created_connector = PrescriptionMedicalTestConnector.objects.first()
        self.assertEqual(created_connector.prescription, self.prescription)
        self.assertEqual(created_connector.test.uuid, self.medical_test.uuid)

    def test_create_prescription_medicine_connector_as_authenticated_user(self):
        self.client.force_authenticate(user=self.doctor_user)
        data = {"medicine": self.medicine.uuid}
        url = reverse(
            "doctor-appointments-Prescription-medicine",
            kwargs={
                "appointment_uuid": self.appointment.uuid,
                "prescription_uuid": self.prescription.uuid,
            },
        )
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrescriptionMedicineConnector.objects.count(), 1)
        created_connector = PrescriptionMedicineConnector.objects.first()
        self.assertEqual(created_connector.prescription, self.prescription)
        self.assertEqual(created_connector.medicine.uuid, self.medicine.uuid)

    def test_retrieve_prescription_as_authenticated_user(self):
        self.client.force_authenticate(user=self.doctor_user)
        url = reverse(
            "doctor-appointments-Prescription-detail",
            kwargs={
                "appointment_uuid": self.appointment.uuid,
                "prescription_uuid": self.prescription.uuid,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        serialized_prescription = PrescriptionSerializer(self.prescription).data
        self.assertEqual(data, serialized_prescription)

    def test_retrieve_prescription_as_unauthorized_user(self):
        unauthorized_user = User.objects.create_user(
            password="unauthorizedpassword",
            email="unauthorized@example.com",
            contact_number="+1355766",
        )
        self.client.force_authenticate(user=unauthorized_user)
        url = reverse(
            "doctor-appointments-Prescription-detail",
            kwargs={
                "appointment_uuid": self.appointment.uuid,
                "prescription_uuid": self.prescription.uuid,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# -----------------------------------------------------------


class DoctorScheduleDaysConnectorTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            password="testpassword", email="test@example.com"
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
        self.hospital_user = UserHospitalRole.objects.create(
            hospital=self.hospital, user=self.user
        )
        self.role = HospitalRole.objects.create(role="Admin")

        self.user_hospital_role = UserHospitalRoleConnector.objects.create(
            hospital_user=self.hospital_user, role=self.role
        )
        self.doctor = Doctor.objects.create(
            doctor_info=self.user,
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
        self.client = APIClient()

    def test_create_doctor_schedule_days_connector_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "doctor_schedule": {
                "doctor": self.doctor.uuid,
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "activity_type": "patient_exam",
                "maximum_patient": 10,
            },
            "day": self.days.uuid,
        }
        url = reverse(
            "create-doctor-schedule-with-day",
            kwargs={"hospital_uuid": self.doctor_schedule.hospital.uuid},
        )
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DoctorScheduleDaysConnector.objects.count(), 1)
        created_connector = DoctorScheduleDaysConnector.objects.first()
        self.assertEqual(created_connector.doctor_schedule, self.doctor_schedule)
        self.assertEqual(created_connector.day, self.days)

    def test_retrieve_doctor_schedule_days_connector_as_authenticated_user(self):
        connector = DoctorScheduleDaysConnector.objects.create(
            doctor_schedule=self.doctor_schedule,
            day=self.days,
        )
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "doctor-schedule-with-day-details",
            kwargs={
                "hospital_uuid": self.hospital.uuid,
                "schedule_uuid": connector.uuid,
            },
        )
        response = self.client.get(
            url,
            kwargs={
                "hospital_uuid": self.doctor_schedule.hospital.uuid,
                "schedule_uuid": connector.uuid,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        expected_data = PrivateDoctorScheduleDaysConnectorSerializer(connector).data
        self.assertEqual(data, expected_data)

    def test_delete_doctor_schedule_days_connector_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        self.connector = DoctorScheduleDaysConnector.objects.create(
            doctor_schedule=self.doctor_schedule,
            day=self.days,
        )
        url = reverse(
            "doctor-schedule-with-day-details",
            kwargs={
                "hospital_uuid": self.hospital.uuid,
                "schedule_uuid": self.connector.uuid,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            DoctorScheduleDaysConnector.objects.filter(id=self.connector.id).exists()
        )
        print("finish")

    # def test_update_doctor_schedule_days_connector_as_authenticated_user(self):
    #     self.client.force_authenticate(user=self.user)
    #     # Create a DoctorScheduleDaysConnector
    #     self.connector = DoctorScheduleDaysConnector.objects.create(
    #         doctor_schedule=self.doctor_schedule,
    #         day=self.days,
    #     )
    #     print()

    #     updated_data = {
    #         "doctor_schedule": {
    #             "doctor": self.doctor.uuid,
    #             "start_time": "15:00:00",
    #             "end_time": "17:00:00",
    #             "activity_type": "patient_exam",
    #             "maximum_patient": 20,
    #         },
    #         "day": self.days.uuid,
    #     }
    #     url = reverse(
    #         "doctor-schedule-with-day-details",
    #         kwargs={
    #             "hospital_uuid": self.hospital.uuid,
    #             "schedule_uuid": self.connector.uuid,
    #         },
    #     )
    #     response = self.client.put(url, updated_data, format="json")
    #     print("response", response, response.data, "*************************")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     updated_connector = DoctorScheduleDaysConnector.objects.get(
    #         id=self.connector.id
    #     )
    #     self.assertEqual(
    #         updated_connector.doctor_schedule.id, updated_data["doctor_schedule"]
    #     )
    #     self.assertEqual(updated_connector.day.id, updated_data["day"])


class DoctorTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )

        self.doctor = Doctor.objects.create(
            doctor_info=self.user,
            department="Cardiology",
            designation="Cardiologist",
            degrees="MBBS, MD",
            medical_school="Medical School",
            license_number="12345",
            license_expiry_date="2023-12-31",
            emergency_contact="1234567890",
            languages_spoken="English, Spanish",
        )
        self.client = APIClient()

    def test_retrieve_doctor_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("doctor-detail", kwargs={"doctor_uuid": self.doctor.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        expected_data = PrivateDoctorSerializer(self.doctor).data
        self.assertEqual(data, expected_data)

    def test_update_doctor_profile_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        updated_data = {
            "department": "Pediatrics",
            "designation": "Pediatrician",
            "degrees": "MBBS, MD, PhD",
            "medical_school": "Pediatric School",
            "license_number": "54321",
            "license_expiry_date": "2024-12-31",
            "emergency_contact": "9876543210",
            "languages_spoken": "English, French",
        }
        url = reverse("doctor-detail", kwargs={"doctor_uuid": self.doctor.uuid})
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_doctor = Doctor.objects.get(uuid=self.doctor.uuid)
        self.assertEqual(updated_doctor.department, updated_data["department"])
        self.assertEqual(updated_doctor.designation, updated_data["designation"])

    def test_create_doctor_profile_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        user = User.objects.create_user(
            email="test2@example.com", password="testpassword", contact_number="+123456"
        )
        data = {
            "doctor_info": user.uuid,
            "department": "Cardiology",
            "designation": "Cardiologist",
            "degrees": "MBBS, MD",
            "medical_school": "Medical School",
            "license_number": "12345",
            "license_expiry_date": "2023-12-31",
            "emergency_contact": "1234567890",
            "languages_spoken": "English, Spanish",
        }
        url = reverse("doctor-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Doctor.objects.count(), 2)
        created_doctor = Doctor.objects.first()
        self.assertEqual(created_doctor.department, data["department"])
        self.assertEqual(created_doctor.designation, data["designation"])
        self.assertEqual(created_doctor.degrees, data["degrees"])

    def test_retrieve_doctor_profile_unauthenticated(self):
        url = reverse("doctor-detail", kwargs={"doctor_uuid": self.doctor.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
