from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from Accounts.models import User
from .models import Days, HospitalRole, Medicine
from .serializers import (
    HospitalRoleSerializer,
    MedicineSerializer,
    PrivateDaysSerializer,
)


class MedicineListCreateTestCase(APITestCase):
    def setUp(self):
        self.super_user = User.objects.create_superuser(
            email="super@gmail.com",
            password="adminpassword",
        )

        self.general_user = User.objects.create_user(
            email="general@gmail.com",
            password="userpassword",
            contact_number="+01234567",
        )
        self.medicine1 = Medicine.objects.create(
            name="Medicine 1",
            dosage="10mg",
            duration="7 days",
            method_of_taken="Orally",
            morning=True,
            noon=False,
            evening=True,
            price=9.99,
        )

        self.medicine2 = Medicine.objects.create(
            name="Medicine 2",
            dosage="20mg",
            duration="14 days",
            method_of_taken="Intravenously",
            morning=False,
            noon=True,
            evening=False,
            price=19.99,
        )
        self.client = APIClient()

    def test_list_medicines_as_super(self):
        self.client.force_authenticate(user=self.super_user)
        url = reverse("medicine-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        expected_data = MedicineSerializer(
            [self.medicine2, self.medicine1], many=True
        ).data
        self.assertEqual(data, expected_data)

    def test_create_medicine_as_super(self):
        self.client.force_authenticate(user=self.super_user)
        data = {
            "name": "New Medicine",
            "dosage": "5mg",
            "duration": "10 days",
            "method_of_taken": "Orally",
            "morning": True,
            "noon": False,
            "evening": True,
            "price": 12.34,
        }
        url = reverse("medicine-list-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medicine.objects.count(), 3)

    def test_retrieve_medicine_as_super(self):
        self.client.force_authenticate(user=self.super_user)
        url = reverse("medicine-detail", kwargs={"medicine_uuid": self.medicine1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        expected_data = MedicineSerializer(self.medicine1).data
        self.assertEqual(data, expected_data)

    def test_update_medicine_as_super(self):
        self.client.force_authenticate(user=self.super_user)
        updated_data = {
            "name": "Updated Medicine 2",
            "dosage": "30mg",
            "duration": "21 days",
            "method_of_taken": "Intravenously",
            "morning": True,
            "noon": True,
            "evening": True,
            "price": 29.99,
        }
        url = reverse("medicine-detail", kwargs={"medicine_uuid": self.medicine2.uuid})
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_medicine2 = Medicine.objects.get(uuid=self.medicine2.uuid)
        self.assertEqual(updated_medicine2.name, updated_data["name"])
        self.assertEqual(updated_medicine2.dosage, updated_data["dosage"])

    def test_create_medicine_as_general_user(self):
        self.client.force_authenticate(user=self.general_user)
        url = reverse("medicine-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Medicine.objects.count(), 2)


class DaysApiTestCase(APITestCase):
    def setUp(self):
        # Create a superuser for testing (Super user)
        self.super_user = User.objects.create_superuser(
            email="super@gmail.com", password="superpassword"
        )

        # Create a general user for testing
        self.general_user = User.objects.create_user(
            email="general@gmail.com",
            password="userpassword",
            contact_number="+01234567",
        )

        # Create some sample Days objects
        self.day1 = Days.objects.create(day="Sunday")
        self.day2 = Days.objects.create(day="Monday")
        self.client = APIClient()

    def test_create_private_day(self):
        self.client.force_authenticate(user=self.super_user)
        data = {"day": "Tuesday"}
        url = reverse("days-list-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Days.objects.count(), 3)

    def test_list_private_days(self):
        self.client.force_authenticate(user=self.super_user)
        url = reverse("days-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Days.objects.count(), 2)

    def test_retrieve_private_day_as_admin(self):
        self.client.force_authenticate(user=self.super_user)
        url = reverse("day-detail", kwargs={"day_uuid": self.day1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        expected_data = PrivateDaysSerializer(self.day1).data
        self.assertEqual(data, expected_data)

    def test_update_private_day_as_admin(self):
        self.client.force_authenticate(user=self.super_user)
        updated_data = {"day": "Updated Day 2"}
        url = reverse("day-detail", kwargs={"day_uuid": self.day2.uuid})
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_day2 = Days.objects.get(uuid=self.day2.uuid)
        self.assertEqual(updated_day2.day, updated_data["day"])

    def test_create_private_day_as_general_user(self):
        # Authenticate as the general user
        self.client.force_authenticate(user=self.general_user)
        data = {"day": "Friday"}
        url = reverse("days-list-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Days.objects.count(), 2)


class HospitalRolesApiTestCase(APITestCase):
    def setUp(self):
        # Create a superuser for testing (Super user)
        self.super_user = User.objects.create_superuser(
            email="super@gmail.com", password="superpassword"
        )

        # Create a general user for testing
        self.general_user = User.objects.create_user(
            email="general@gmail.com",
            password="userpassword",
            contact_number="+01234567",
        )

        # Create some sample Role objects
        self.role1 = HospitalRole.objects.create(role="Doctor")
        self.role2 = HospitalRole.objects.create(role="Nurse")
        self.client = APIClient()

    def test_create_role(self):
        self.client.force_authenticate(user=self.super_user)
        data = {"role": "Staff"}
        url = reverse("hospital-role-list-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HospitalRole.objects.count(), 3)

    def test_list_role(self):
        self.client.force_authenticate(user=self.super_user)
        url = reverse("hospital-role-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HospitalRole.objects.count(), 2)

    def test_retrieve_role_as_admin(self):
        self.client.force_authenticate(user=self.super_user)
        url = reverse("hospital-role-detail", kwargs={"role_uuid": self.role1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        expected_data = HospitalRoleSerializer(self.role1).data
        self.assertEqual(data, expected_data)

    def test_update_role_as_admin(self):
        self.client.force_authenticate(user=self.super_user)
        updated_data = {"role": "Updated role 2"}
        url = reverse("hospital-role-detail", kwargs={"role_uuid": self.role2.uuid})
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_role2 = HospitalRole.objects.get(uuid=self.role2.uuid)
        self.assertEqual(updated_role2.role, updated_data["role"])

    def test_create_role_as_general_user(self):
        # Authenticate as the general user
        self.client.force_authenticate(user=self.general_user)
        data = {"role": "Staff"}
        url = reverse("hospital-role-list-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(HospitalRole.objects.count(), 2)
