from django.shortcuts import get_object_or_404
from django.core.cache import cache

from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from Accounts.permissions import IsLoggedIn, authenticateUser

from Doctor.models import Doctor, DoctorScheduleDaysConnector

from Hospital.models import Hospital, UserHospitalRoleConnector
from Hospital.permissions import IsHospitalAdmin


from .models import (
    DoctorAppointment,
    Prescription,
)

from .serializers import (
    DoctorAppointmentUpdateDeleteSerializer,
    DoctorAppointmentSerializer,
    HospitalListSerializer,
    HospitalDoctorListSerializer,
    HospitalDoctorScheduleSerializer,
    HospitalDoctorScheduleAppointmentSerializer,
    PrescriptionSerializer,
    PatientPrescriptionDetailSerializer,
    PrescriptionListSerializer,
)


class HospitalDoctorScheduleAppointmentPrescriptionDetail(RetrieveAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        email = self.request.user.email
        prescription_uuid = self.kwargs.get("prescription_uuid")
        obj = Prescription.objects.filter(
            uuid=prescription_uuid, patient_doctor_booking__patient__email=email
        ).first()

        return obj


class HospitalDoctorScheduleAppointmentPrescription(ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        email = self.request.user.email
        appointment_uuid = self.kwargs.get("appointment_uuid")
        queryset = Prescription.objects.filter(
            patient_doctor_booking__patient__email=email,
            patient_doctor_booking__uuid=appointment_uuid,
        )
        return queryset


class HospitalDoctorScheduleAppointmentDetail(RetrieveAPIView):
    serializer_class = HospitalDoctorScheduleAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        appointment_uuid = self.kwargs.get("appointment_uuid")
        queryset = DoctorAppointment.objects.filter(
            uuid=appointment_uuid, patient=user
        ).first()

        return queryset


# -------------- Appointment -----------------


# Only Hospital admin can update or cancel appointment
class DoctorAppointmentRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorAppointmentUpdateDeleteSerializer
    permission_classes = [IsAuthenticated, IsHospitalAdmin]

    def get_object(self):
        uuid = self.kwargs.get("appointment_uuid")
        queryset = DoctorAppointment.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


# Patient can appoint of Doctor appointment
class PatientDoctorAppointmentListCreate(ListCreateAPIView):
    serializer_class = DoctorAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        # Pass the request context to the serializer

        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        print(self.request.user.email)
        queryset = DoctorAppointment.objects.select_related(
            "doctor_schedule_day"
        ).filter(patient__email=self.request.user.email)
        return queryset


class HospitalDoctorSchedule(ListAPIView):
    serializer_class = HospitalDoctorScheduleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        hospital_uuid = self.kwargs.get("hospital_uuid")
        doctor_uuid = self.kwargs.get("doctor_uuid")
        queryset = DoctorScheduleDaysConnector.objects.select_related(
            "doctor_schedule",
            "doctor_schedule__hospital",
            "doctor_schedule__doctor",
            "doctor_schedule__doctor__doctor_info",
            "day",
        ).filter(
            doctor_schedule__hospital__uuid=hospital_uuid,
            doctor_schedule__doctor__uuid=doctor_uuid,
        )
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
        hospital_uuid = self.kwargs.get("hospital_uuid")
        queryset = (
            UserHospitalRoleConnector.objects.select_related("hospital_user", "role")
            .prefetch_related(
                "hospital_user__user",
                "hospital_user__hospital",
            )
            .filter(hospital_user__hospital__uuid=hospital_uuid, role__role="Doctor")
        )
        return queryset


class HospitalList(ListAPIView):
    serializer_class = HospitalListSerializer
    permission_classes = [AllowAny]

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["hospital_name"]

    cache_key = "hospital_list"

    def get_queryset(self):
        queryset = cache.get(self.cache_key)
        if queryset is None:
            queryset = Hospital.objects.all()
            cache.set(self.cache_key, queryset, 24 * 3600)
        return queryset
