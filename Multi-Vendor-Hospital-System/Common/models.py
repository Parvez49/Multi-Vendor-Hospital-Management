from django.db import models

# Create your models here.

from dirtyfields import DirtyFieldsMixin
import uuid


class BaseModelWithUID(DirtyFieldsMixin, models.Model):
    uuid = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def get_auto_fields(self):
        fields = [
            "updated_at",
        ]
        return fields


# helper model represent day name such as Friday, Saturday ... etc
class Days(BaseModelWithUID):
    day = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.day


# users can have at hospitals (e.g., Admin, Doctor, Nurse, Staff
class HospitalRole(BaseModelWithUID):
    role = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.role


# helper model represent medical specialties such as cardiology, pediatrics, orthopedics, etc.
class Specialty(BaseModelWithUID):
    specialty = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.specialty


class Medicine(BaseModelWithUID):
    name = models.TextField(max_length=100, unique=True)
    dosage = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)
    method_of_taken = models.CharField(
        max_length=50
    )  # How the medication should be taken (e.g., orally, intravenously).
    morning = models.BooleanField(blank=True)
    noon = models.BooleanField(blank=True)
    evening = models.BooleanField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Medical_Test(BaseModelWithUID):
    name = models.TextField(max_length=100, unique=True)
    process = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name
