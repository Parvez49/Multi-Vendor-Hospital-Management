# ------------------------ Test Case for Registration --------------------
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import PublicUserListSerializer  # Import your serializer
from .models import User  # Import your User model
from .tasks import send_verification_email  # Import your Celery task
from celery import Celery
from celery.contrib.testing.worker import start_worker
from celery.result import AsyncResult

# from django_celery_beat.test_utils import CeleryTestCase


class PublicUserCreateTestCase(APITestCase):
    def setUp(self):
        self.app = Celery("Multi_Vendor_Medical_System")  # Replace with your app name
        self.worker = self.app.Worker()
        self.worker.start()

    def tearDown(self):
        self.worker.stop()

    def test_user_registration(self):
        url = reverse("user-register")  # Replace with the actual URL name

        # Define the registration data
        registration_data = {
            "email": "test@example.com",
            "password": "pass",
            "gender": "male",
            "blood_group": "B+",
            "nationality": "BD",
            "contact_number": "+012344556"
            # Add other required registration fields as needed
        }

        response = self.client.post(url, registration_data, format="json")
        print("respionse code: ", response.status_code)  # Add this line for debugging
        print("content", response.content)  # Add this line for debugging

        # Check that the response has a status code of 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the user object was created in the database
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

        # Assert that the Celery task was called
        self.worker.join()  # Wait for the task to complete
        self.assertTrue(send_verification_email.delay.called)

        # Optionally, you can check that the task was called with the correct arguments
        self.assertTrue(
            send_verification_email.delay.call_args[0][0] == "test@example.com"
        )

        # Check the response message
        self.assertEqual(
            response.data["message"],
            "Account created. Check your email to activate your account.",
        )
"""
