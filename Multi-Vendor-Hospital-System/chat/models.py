from django.db import models

from Accounts.models import User
from Doctor.models import Doctor


class Message(models.Model):
    patient = models.ForeignKey(to=User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content}"
