from django.db import models

# Create your models here.

from Common.models import BaseModelWithUID

from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

from versatileimagefield.fields import VersatileImageField
from versatileimagefield.fields import PPOIField


class BloodGroups(models.TextChoices):
    NOT_SET = "Not Set", "Not Set"
    A_POSITIVE = "A+", "A+"
    A_NEGATIVE = "A-", "A-"
    B_POSITIVE = "B+", "B+"
    B_NEGATIVE = "B-", "B-"
    AB_POSITIVE = "AB+", "AB+"
    AB_NEGATIVE = "AB-", "AB-"
    O_POSITIVE = "O+", "O+"
    O_NEGATIVE = "O-", "O-"


class User(AbstractUser, BaseModelWithUID):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    blood_group = models.CharField(
        max_length=10,
        blank=True,
        choices=BloodGroups.choices,
        default=BloodGroups.NOT_SET,
    )
    nationality = models.CharField(max_length=100)
    contact_number = PhoneNumberField(
        blank=True, db_index=True, verbose_name="Phone Number"
    )
    # profile_picture = models.ImageField(upload_to="user_profiles/", blank=True)
    profile_picture = VersatileImageField(
        "Headshot",
        upload_to="headshots/",
        ppoi_field="headshot_ppoi",
        default="placeholder/man.jpg",  # Set the default placeholder image path
    )
    headshot_ppoi = PPOIField()

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Notification(BaseModelWithUID, models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_head = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.recipient.email + " " + str(self.uuid)
