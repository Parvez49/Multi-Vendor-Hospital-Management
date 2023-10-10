from django.core.management.base import BaseCommand

from Accounts.models import User


class Command(BaseCommand):
    help = "List all Common Model data in the database"

    def handle(self, *args, **kwargs):
        user_list = {
            "users": [
                {
                    "email": "john@gmail.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "gender": "Male",
                    "date_of_birth": "1990-05-15",
                    "height": 175.5,
                    "weight": 70,
                    "blood_group": "A+",
                    "nationality": "American",
                    "contact_number": "+1 (123) 456-7890",
                },
                {
                    "email": "alice@gmail.com",
                    "first_name": "Alice",
                    "last_name": "Smith",
                    "gender": "Female",
                    "date_of_birth": "1985-08-20",
                    "height": 162.3,
                    "weight": 58,
                    "blood_group": "B-",
                    "nationality": "British",
                    "contact_number": "+44 20 7123 4567",
                },
                {
                    "email": "david@gmail.com",
                    "first_name": "David",
                    "last_name": "Johnson",
                    "gender": "Male",
                    "date_of_birth": "1995-03-10",
                    "height": 180.0,
                    "weight": 80,
                    "blood_group": "O+",
                    "nationality": "Canadian",
                    "contact_number": "+1 (604) 555-1234",
                },
                {
                    "email": "emily@gmail.com",
                    "first_name": "Emily",
                    "last_name": "Brown",
                    "gender": "Female",
                    "date_of_birth": "1988-11-25",
                    "height": 167.7,
                    "weight": 63,
                    "blood_group": "AB+",
                    "nationality": "Australian",
                    "contact_number": "+61 2 9876 5432",
                },
                {
                    "email": "michael@gmail.com",
                    "first_name": "Michael",
                    "last_name": "Lee",
                    "gender": "Male",
                    "date_of_birth": "1992-07-02",
                    "height": 185.2,
                    "weight": 75,
                    "blood_group": "A-",
                    "nationality": "German",
                    "contact_number": "+49 30 12345 6789",
                },
            ]
        }
        for user in user_list["users"]:
            User.objects.get_or_create(**user)
