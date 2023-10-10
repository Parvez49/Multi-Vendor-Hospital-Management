from django.core.management.base import BaseCommand

from Common.models import Days, HospitalRole, Specialty, Medical_Test, Medicine


class Command(BaseCommand):
    help = "List all Common Model data in the database"

    def handle(self, *args, **kwargs):
        self.insert_into_day()
        self.insert_into_hopital_role()
        self.insert_into_specialty()
        self.insert_into_medicine()
        self.insert_into_medical_test()

        self.get_medical_test()
        self.get_medicines()
        self.get_specialty()
        self.get_hospital_role()
        self.get_day_data()

    def insert_into_medical_test(self):
        tests = {
            "test1": {
                "name": "Blood Sugar",
                "process": "Test Description",
                "price": 200,
            },
            "test2": {
                "name": "Blood Group ",
                "process": "process of blood group",
                "price": 300,
            },
            "test3": {
                "name": "Blood Film",
                "process": "process of blood film",
                "price": 350,
            },
            "test4": {
                "name": "Brain Plain",
                "process": "process of blood film",
                "price": 3500,
            },
        }
        for key in tests:
            Medical_Test.objects.get_or_create(**tests[key])

    def get_medical_test(self):
        tests = Medical_Test.objects.all()
        if tests:
            self.stdout.write("List of Medical Tests:")
            for tst in tests:
                self.stdout.write(self.style.SUCCESS(tst.name))
        else:
            self.stdout.write(
                self.style.WARNING("No Medical Test found in the database")
            )

    def insert_into_medicine(self):
        medicines = {
            "medicine1": {
                "name": "Paracetamol",
                "dosage": "500mg",
                "duration": "5 days",
                "method_of_taken": "Orally",
                "morning": True,
                "noon": False,
                "evening": True,
                "price": 2.99,
            },
            "medicine2": {
                "name": "Amoxicillin",
                "dosage": "250mg",
                "duration": "10 days",
                "method_of_taken": "Orally",
                "morning": True,
                "noon": True,
                "evening": True,
                "price": 5.49,
            },
            "medicine3": {
                "name": "Lisinopril",
                "dosage": "10mg",
                "duration": "30 days",
                "method_of_taken": "Orally",
                "morning": True,
                "noon": False,
                "evening": True,
                "price": 7.99,
            },
            "medicine4": {
                "name": "Omeprazole",
                "dosage": "20mg",
                "duration": "14 days",
                "method_of_taken": "Orally",
                "morning": False,
                "noon": True,
                "evening": True,
                "price": 4.75,
            },
            "medicine5": {
                "name": "Atorvastatin",
                "dosage": "40mg",
                "duration": "60 days",
                "method_of_taken": "Orally",
                "morning": True,
                "noon": True,
                "evening": True,
                "price": 11.25,
            },
        }

        for key in medicines:
            Medicine.objects.get_or_create(**medicines[key])

    def get_medicines(self):
        medicines = Medicine.objects.all()
        if medicines:
            self.stdout.write("List of Medicines:")
            for mdc in medicines:
                self.stdout.write(self.style.SUCCESS(mdc.name))
        else:
            self.stdout.write(self.style.WARNING("No Medicine found in the database"))

    def insert_into_specialty(self):
        spcialties = ["cardiology", "pediatrics", "orthopedics", "Neurology", "Surgery"]
        for spc in spcialties:
            Specialty.objects.get_or_create(specialty=spc)

    def get_specialty(self):
        specialties = Specialty.objects.all()
        if specialties:
            self.stdout.write("List of Hospital Specilaty:")
            for spc in specialties:
                self.stdout.write(self.style.SUCCESS(spc.specialty))
        else:
            self.stdout.write(self.style.WARNING("No specialty found in the database"))

    def insert_into_hopital_role(self):
        roles = ["Admin", "Doctor", "Nurse", "Staff"]
        for role in roles:
            HospitalRole.objects.get_or_create(role=role)

    def get_hospital_role(self):
        roles = HospitalRole.objects.all()
        if roles:
            self.stdout.write("List of Specialty:")
            for role in roles:
                self.stdout.write(self.style.SUCCESS(role.role))
        else:
            self.stdout.write(self.style.WARNING("No roles found in the database"))

    def get_day_data(self):
        days = Days.objects.all()

        if days:
            self.stdout.write("List of days:")
            for day in days:
                self.stdout.write(self.style.SUCCESS(day.day))
        else:
            self.stdout.write(self.style.WARNING("No days found in the database"))

    def insert_into_day(self):
        days = [
            "Saturday",
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
        ]

        for day in days:
            Days.objects.get_or_create(day=day)
            # day, created = Days.objects.get_or_create(day=day_name)
            # if created:
            #     self.stdout.write(self.style.SUCCESS(f"Created and inserted: {day.day}"))
            # else:
            #     self.stdout.write(self.style.WARNING(f"Day already exists: {day.day}"))
