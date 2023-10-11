from django.shortcuts import get_object_or_404


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
