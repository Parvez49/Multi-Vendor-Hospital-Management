from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from Accounts.models import User
from .models import Founder, Hospital
from .serializers import PrivateFounderSerializer, PrivateHospitalSerializer


class HospitalTestCase(APITestCase):
    def setUp(self):
        # Create a superuser for testing (admin user)
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )

        # Create some sample Hospital objects
        self.hospital1 = Hospital.objects.create(
            registration_no="123456",
            hospital_name="Hospital 1",
            logo="/hospital_logos/hospitallogo.png",
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

        self.hospital2 = Hospital.objects.create(
            registration_no="789012",
            hospital_name="Hospital 2",
            logo="/hospital_logos/hospitallogo2.png",
            city="City 2",
            state="State 2",
            postal_code="67890",
            country="Country 2",
            contact_number="9876543210",
            operating_hours="9:00 AM - 6:00 PM",
            description="Description 2",
            additional_notes="Additional Notes 2",
            facilities="Facilities 2",
        )

        self.client = APIClient()

    def test_retrieve_hospital_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        # Get the URL for your view using reverse, passing the UUID of hospital1
        url = reverse("hospital-detail", kwargs={"hospital_uuid": self.hospital1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_hospital_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        updated_data = {
            "hospital_name": "Updated Hospital 2",
            "city": "Updated City 2",
            "state": "Updated State 2",
        }
        # Get the URL for your view using reverse, passing the UUID of hospital2
        url = reverse("hospital-detail", kwargs={"hospital_uuid": self.hospital2.uuid})
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_hospital2 = Hospital.objects.get(uuid=self.hospital2.uuid)
        # Check if the hospital was updated correctly
        self.assertEqual(updated_hospital2.hospital_name, updated_data["hospital_name"])
        self.assertEqual(updated_hospital2.city, updated_data["city"])

    def test_list_hospitals_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("hospital-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_hospital_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "registration_no": "987654",
            "hospital_name": "New Hospital",
            "city": "New City",
            "state": "New State",
            "postal_code": "54321",
            "country": "New Country",
            "contact_number": "1234567890",
            "operating_hours": "8:00 AM - 5:00 PM",
            "description": "Description for New Hospital",
            "additional_notes": "Additional Notes for New Hospital",
            "facilities": "Facilities for New Hospital",
        }
        url = reverse("hospital-list-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hospital.objects.count(), 3)
        created_hospital = Hospital.objects.get(registration_no="987654")

        # Check if the created Hospital matches the input data
        self.assertEqual(created_hospital.registration_no, data["registration_no"])
        self.assertEqual(created_hospital.hospital_name, data["hospital_name"])
        self.assertEqual(created_hospital.city, data["city"])
        self.assertEqual(created_hospital.state, data["state"])

    def test_create_hospital_unauthorized(self):
        # Don't authenticate, simulating an unauthorized request
        data = {
            "registration_no": "987654",
            "hospital_name": "New Hospital",
            "city": "New City",
            "state": "New State",
            "postal_code": "54321",
            "country": "New Country",
            "contact_number": "1234567890",
            "operating_hours": "8:00 AM - 5:00 PM",
            "description": "Description for New Hospital",
            "additional_notes": "Additional Notes for New Hospital",
            "facilities": "Facilities for New Hospital",
        }
        url = reverse("hospital-list-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Hospital.objects.count(), 2)


class FounderTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )
        self.general_user = User.objects.create_user(
            email="general@gmail.com",
            password="userpassword",
            contact_number="+01234567",
        )

        # Create some sample Hospital objects
        self.hospital1 = Hospital.objects.create(
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

        # Create some sample Founder objects
        self.founder1 = Founder.objects.create(
            founder=self.admin_user,
            hospital=self.hospital1,
        )
        self.client = APIClient()

    def test_retrieve_founder_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("founder-detail", kwargs={"founder_uuid": self.founder1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        expected_data = PrivateFounderSerializer(self.founder1).data
        self.assertEqual(data, expected_data)

    def test_list_founders_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("founder-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        expected_data = PrivateFounderSerializer([self.founder1], many=True).data
        self.assertEqual(data, expected_data)
