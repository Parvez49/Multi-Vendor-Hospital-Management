from django.db import models

from autoslug import AutoSlugField

# Create your models here.

from Accounts.models import User, BaseModelWithUID
from Common.models import Specialty, HospitalRole
from phonenumber_field.modelfields import PhoneNumberField

#  --------------- Hospital Registration -----------------


class Hospital(BaseModelWithUID, models.Model):
    registration_no = models.CharField(max_length=255, unique=True)
    hospital_name = models.CharField(max_length=255)  # official name of the hospital
    slug = AutoSlugField(populate_from="hospital_name", unique=True)
    logo = models.ImageField(upload_to="hospital_logos/", blank=True)

    # Location of hospital
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    # Contact Information
    contact_number = PhoneNumberField(db_index=True, verbose_name="Phone Number")
    website = models.URLField(blank=True)

    # About Hospital
    description = (
        models.TextField()
    )  # A brief description or mission statement for the hospital
    additional_notes = models.TextField(blank=True)

    # Services
    operating_hours = models.TextField()
    insurance_accepted = models.TextField(blank=True)
    facilities = (
        models.TextField()
    )  # the facilities and amenities available at the hospital, such as parking, cafeteria, pharmacy, etc.

    def __str__(self):
        return self.hospital_name


# Information about the founders or owners of the hospital
class Founder(BaseModelWithUID, models.Model):
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.founder.first_name + " " + self.hospital.hospital_name


# such as cardiology, pediatrics, orthopedics, etc.
class HospitalSpecialtyConnector(BaseModelWithUID, models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)


class UserHospitalRole(BaseModelWithUID, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    # roles = models.ManyToManyField(HospitalRole)

    def __str__(self):
        return (
            str(self.hospital.hospital_name)
            + " "
            + str(self.user.first_name)
            + " "
            + str(self.user.last_name)
        )


class UserHospitalRoleConnector(BaseModelWithUID, models.Model):
    hospital_user = models.ForeignKey(UserHospitalRole, on_delete=models.CASCADE)
    role = models.ForeignKey(HospitalRole, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.uuid)
