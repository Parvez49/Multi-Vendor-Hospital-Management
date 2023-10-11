from rest_framework.permissions import BasePermission
from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from .models import Hospital, UserHospitalRoleConnector


class IsHospitalAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        slug = view.kwargs.get("hospital_slug")
        hospital = Hospital.objects.filter(slug=slug).first()
        if not hospital:
            raise ValidationError("Wrong hospital uuid!!!")
        if UserHospitalRoleConnector.objects.filter(
            hospital_user__user=user,
            hospital_user__hospital=hospital,
            role__role="Admin",
        ).exists():
            return True
        else:
            raise PermissionDenied("You have no permission!!!")
