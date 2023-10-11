from django.shortcuts import get_object_or_404
from django.core.cache import cache

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from Doctor.models import DoctorScheduleDaysConnector, EmergencyDoctorScedule
from .models import (
    Founder,
    Hospital,
    HospitalSpecialtyConnector,
    UserHospitalRoleConnector,
)
from .permissions import IsHospitalAdmin
from .serializers import (
    HospitalDoctorListSerializer,
    HospitalDoctorScheduleSerializer,
    PrivateFounderSerializer,
    PrivateHospitalSerializer,
    PrivateHospitalSpecialtyConnectorSerializer,
    PrivateDoctorScheduleDaysConnectorSerializer,
    PrivateDoctorScheduleDateConnectorSerializer,
    UserHospitalRoleConnectorSerializer,
)

# ------------------ Doctor Schedule with Days -----------------


class PrivateDoctorScheduleDaysConnectorRetrieveUpdateDestroy(
    RetrieveUpdateDestroyAPIView
):
    serializer_class = PrivateDoctorScheduleDaysConnectorSerializer
    permission_classes = [IsHospitalAdmin]

    def get_object(self):
        uuid = self.kwargs.get("schedule_uuid")
        queryset = DoctorScheduleDaysConnector.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


class PrivateDoctorScheduleDaysConnectorListCreate(ListCreateAPIView):
    serializer_class = PrivateDoctorScheduleDaysConnectorSerializer
    permission_classes = [IsHospitalAdmin]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["hospital_slug"] = self.kwargs.get("hospital_slug")
        return context

    def get_queryset(self):
        slug = self.kwargs.get("hospital_slug")
        hospital = Hospital.objects.filter(slug=slug).first()
        queryset = DoctorScheduleDaysConnector.objects.filter(
            doctor_schedule__hospital=hospital
        )
        return queryset


# ------------------ Doctor Schedule with Date -----------------


class PrivateDoctorScheduleDateConnectorRetrieveUpdateDestroy(
    RetrieveUpdateDestroyAPIView
):
    serializer_class = PrivateDoctorScheduleDateConnectorSerializer
    permission_classes = [IsHospitalAdmin]

    def get_object(self):
        uuid = self.kwargs.get("schedule_uuid")
        queryset = EmergencyDoctorScedule.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


class PrivateDoctorScheduleDateConnectorListCreate(ListCreateAPIView):
    serializer_class = PrivateDoctorScheduleDateConnectorSerializer
    permission_classes = [IsHospitalAdmin]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["hospital_slug"] = self.kwargs.get("hospital_slug")
        return context

    def get_queryset(self):
        slug = self.kwargs.get("hospital_slug")
        hospital = Hospital.objects.filter(slug=slug).first()
        queryset = EmergencyDoctorScedule.objects.filter(
            doctor_schedule__hospital=hospital
        )
        return queryset


class HospitalDoctorSchedule(ListAPIView):
    serializer_class = HospitalDoctorScheduleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        hospital_slug = self.kwargs.get("hospital_slug")
        doctor_slug = self.kwargs.get("doctor_slug")
        queryset = DoctorScheduleDaysConnector.objects.select_related(
            "doctor_schedule",
            "doctor_schedule__hospital",
            "doctor_schedule__doctor",
            "doctor_schedule__doctor__doctor_info",
            "day",
        ).filter(
            doctor_schedule__hospital__slug=hospital_slug,
            doctor_schedule__doctor__slug=doctor_slug,
        )
        return queryset


class HospitalDoctorList(ListAPIView):
    serializer_class = HospitalDoctorListSerializer
    permission_classes = [AllowAny]

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = [
        "hospital_user__user__first_name",
        "hospital_user__user__last_name",
    ]

    def get_queryset(self):
        hospital_slug = self.kwargs.get("hospital_slug")
        queryset = (
            UserHospitalRoleConnector.objects.select_related("hospital_user", "role")
            .prefetch_related(
                "hospital_user__user",
                "hospital_user__hospital",
            )
            .filter(hospital_user__hospital__slug=hospital_slug, role__role="Doctor")
        )
        return queryset


class UserHospitalRoleConnectorRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = UserHospitalRoleConnectorSerializer
    permission_classes = [IsHospitalAdmin]

    def get_object(self):
        uuid = self.kwargs.get("user_hospital_role_uuid")
        queryset = UserHospitalRoleConnector.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        return obj


class UserHospitalRoleConnectorListCreate(ListCreateAPIView):
    serializer_class = UserHospitalRoleConnectorSerializer
    permission_classes = [IsAuthenticated, IsHospitalAdmin]

    def get_serializer_context(self):
        # Pass the request context to the serializer
        context = super().get_serializer_context()
        context["hospital_slug"] = self.kwargs["hospital_slug"]
        return context

    def get_queryset(self):
        hospital_slug = self.kwargs["hospital_slug"]
        queryset = UserHospitalRoleConnector.objects.filter(
            hospital_user__hospital__slug=hospital_slug
        )
        return queryset


# ---------------- HospitalSpecialtyConnector ------------------


class PrivateHospitalSpecialtyConnectorRetrieveUpdateDestroy(
    RetrieveUpdateDestroyAPIView
):
    queryset = HospitalSpecialtyConnector.objects.all()
    serializer_class = PrivateHospitalSpecialtyConnectorSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        uuid = self.kwargs.get("specialty_uuid")
        queryset = HospitalSpecialtyConnector.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        return obj


class PrivateHospitalSpecialtyConnectorListCreate(ListCreateAPIView):
    queryset = HospitalSpecialtyConnector.objects.all()
    serializer_class = PrivateHospitalSpecialtyConnectorSerializer
    permission_classes = [IsAdminUser]


# -------------- Founder -----------------


class PrivateFounderRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateFounderSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        uuid = self.kwargs.get("founder_uuid")
        queryset = Founder.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        return obj


class PrivateFounderListCreate(ListCreateAPIView):
    queryset = Founder.objects.all()
    serializer_class = PrivateFounderSerializer
    permission_classes = [IsAdminUser]
    # lookup_field = "uuid"


# ------------- Hospital -------------------


class PrivateHospitalRetrieveUpdateDestroy(RetrieveUpdateAPIView):
    serializer_class = PrivateHospitalSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_object(self):
        slug = self.kwargs.get("hospital_slug")
        queryset = Hospital.objects.filter(slug=slug)
        obj = get_object_or_404(queryset)
        return obj


class PrivateHospitalListCreate(ListCreateAPIView):
    serializer_class = PrivateHospitalSerializer

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["hospital_name"]

    cache_key = "hospital_list"

    def get_permissions(self):
        if self.request.method != "POST":
            return [AllowAny()]  # Allow any for GET requests
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = cache.get(self.cache_key)
        if queryset is None:
            queryset = Hospital.objects.all()
            cache.set(self.cache_key, queryset, 24 * 3600)
        return queryset


"""
DoctorScheduleDaysConnector.objects.filter(
            doctor_schedule__hospital__uuid=hospital_uuid,
            doctor_schedule__doctor__uuid=doctor_uuid,
            )

DoctorScheduleDaysConnector.objects.select_related(
                "doctor_schedule", "day", "doctor_schedule__hospital"
            )
            .prefetch_related("doctor_schedule__doctor")
            .filter(
                doctor_schedule__hospital__uuid=hospital_uuid,
                doctor_schedule__doctor__uuid=doctor_uuid,
            )
DoctorScheduleDaysConnector.objects.select_related(
                "doctor_schedule",
                "day",
            )
            .prefetch_related("doctor_schedule__doctor", "doctor_schedule__hospital")
            .filter(
                doctor_schedule__hospital__uuid=hospital_uuid,
                doctor_schedule__doctor__uuid=doctor_uuid,
            )
"""
