from rest_framework.permissions import BasePermission
from rest_framework.exceptions import (
    PermissionDenied,
    AuthenticationFailed,
    ValidationError,
)
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError

from Accounts.models import User
from Accounts.permissions import authenticateUser
from Patient.models import DoctorAppointment
from Hospital.models import Hospital, UserHospitalRoleConnector


class IsHospitalDoctor(BasePermission):
    def has_permission(self, request, view):
        token = request.COOKIES.get("logintoken")
        payload = authenticateUser(token)
        email = payload["email"]
        user = User.objects.filter(email=email).first()

        # data = request.data["hospital_user"]
        # hospital = Hospital.objects.filter(uuid=data["hospital"]).first()
        uuid = view.kwargs.get("hospital_uuid")
        print(uuid)
        hospital = Hospital.objects.filter(uuid=uuid).first()
        if not hospital:
            raise ValidationError("Wrong hospital uuid!!!")
        if UserHospitalRoleConnector.objects.filter(
            hospital_user__user=user,
            hospital_user__hospital=hospital,
            role__role="Doctor",
        ).exists():
            return True
        else:
            raise PermissionDenied("You have no permission!!!")


class IsAppointmentDoctor(BasePermission):
    def has_permission(self, request, view):
        email = request.user.email
        appointment_uuid = view.kwargs.get("appointment_uuid")
        if DoctorAppointment.objects.filter(
            uuid=appointment_uuid,
            doctor_schedule_day__doctor_schedule__doctor__doctor_info__email=email,
        ).exists():
            return True
        else:
            raise PermissionDenied("You have no permission!!!")
