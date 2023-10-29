from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from Accounts.permissions import IsLoggedIn, authenticateUser
from Common.models import Medical_Test, Medicine
from Common.serializers import MedicalTestSerializer, MedicineSerializer
from Hospital.models import Hospital
from Hospital.permissions import IsHospitalAdmin

from Patient.models import (
    DoctorAppointment,
    Prescription,
    PrescriptionMedicalTestConnector,
    PrescriptionMedicineConnector,
)
from Patient.serializers import (
    PrescriptionSerializer,
    PrescriptionMedicalTestConnectorSerializer,
    PrescriptionMedicineConnectorSerializer,
    DoctorAppointmentSerializer,
)

from .permissions import IsAppointmentDoctor


from .models import (
    Doctor,
    DoctorSpecialtyConnector,
    DoctorScheduleDaysConnector,
    EmergencyDoctorScedule,
)
from .serializers import (
    PrivateDoctorSerializer,
    PrivateDoctorSpecialtyConnectorSerializer,
)

# --------------------- Prescription Medical Test -------------------


class PrescriptionMedicineConnectorListCreate(ListCreateAPIView):
    serializer_class = PrescriptionMedicineConnectorSerializer
    permission_classes = [IsAppointmentDoctor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        prescription_uuid = self.kwargs.get("prescription_uuid")
        context["prescription_uuid"] = prescription_uuid
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = PrescriptionMedicineConnector.objects.select_related(
            "medicine"
        ).filter(
            prescription__patient_doctor_booking__doctor_schedule_day__doctor_schedule__doctor__doctor_info=user
        )
        return queryset


class PrescriptionMedicalTestConnectorListCreate(ListCreateAPIView):
    serializer_class = PrescriptionMedicalTestConnectorSerializer
    permission_classes = [IsAppointmentDoctor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        prescription_uuid = self.kwargs.get("prescription_uuid")
        context["prescription_uuid"] = prescription_uuid
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = PrescriptionMedicalTestConnector.objects.select_related(
            "test"
        ).filter(
            prescription__patient_doctor_booking__doctor_schedule_day__doctor_schedule__doctor__doctor_info=user
        )
        return queryset


# ------------------ Doctor Appointments ------------------


class DoctorAppointmentsPrescriptionDetail(RetrieveAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAppointmentDoctor]

    def get_object(self):
        user = self.request.user
        uuid = self.kwargs.get("prescription_uuid")
        obj = (
            Prescription.objects.select_related("patient_doctor_booking__patient")
            .prefetch_related(
                "prescription_test__test", "prescription_medicine__medicine"
            )
            .filter(
                uuid=uuid,
                patient_doctor_booking__doctor_schedule_day__doctor_schedule__doctor__doctor_info=user,
            )
            .first()
        )
        return obj


class DoctorAppointmentsPrescription(ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsAppointmentDoctor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["patient_doctor_booking"] = self.kwargs.get("appointment_uuid")
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Prescription.objects.select_related("patient_doctor_booking__patient")
            .prefetch_related(
                "prescription_test__test", "prescription_medicine__medicine"
            )
            .filter(
                patient_doctor_booking__doctor_schedule_day__doctor_schedule__doctor__doctor_info=user
            )
        )
        return queryset


class DoctorAppointmentsDetail(RetrieveAPIView):
    serializer_class = DoctorAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_email = self.request.user.email
        uuid = self.kwargs.get("appointment_uuid")
        obj = (
            DoctorAppointment.objects.select_related(
                "doctor_schedule_day",
                "patient",
                "doctor_schedule_day__doctor_schedule",
                "doctor_schedule_day__doctor_schedule__hospital",
                "doctor_schedule_day__doctor_schedule__doctor",
                "doctor_schedule_day__doctor_schedule__doctor__doctor_info",
            )
            .filter(
                uuid=uuid,
                doctor_schedule_day__doctor_schedule__doctor__doctor_info__email=user_email,
            )
            .first()
        )

        return obj


class DoctorAppointmentsList(ListAPIView):
    serializer_class = DoctorAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = DoctorAppointment.objects.select_related(
            "doctor_schedule_day",
            "patient",
            "doctor_schedule_day__doctor_schedule",
            "doctor_schedule_day__doctor_schedule__hospital",
            "doctor_schedule_day__doctor_schedule__doctor",
            "doctor_schedule_day__doctor_schedule__doctor__doctor_info",
        ).filter(
            doctor_schedule_day__doctor_schedule__doctor__doctor_info=self.request.user
        )
        return queryset


# ---------------- Doctor Specialty --------------------


class PrivateDoctorSpecialtyConnectorRetrieveUpdateDestroy(
    RetrieveUpdateDestroyAPIView
):
    serializer_class = PrivateDoctorSpecialtyConnectorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        uuid = self.kwargs.get("doctor_specialty_uuid")
        queryset = DoctorSpecialtyConnector.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


class PrivateDoctorSpecialtyConnectorListCreate(ListCreateAPIView):
    serializer_class = PrivateDoctorSpecialtyConnectorSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        print("context")
        user = self.request.user
        context = super().get_serializer_context()
        context["user"] = user
        return context

    def get_queryset(self):
        print("queryset")
        queryset = DoctorSpecialtyConnector.objects.select_related(
            "doctor", "doctor__doctor_info", "specialty"
        ).filter(doctor__doctor_info=self.request.user)
        return queryset


# --------------- Doctor Registration ------------------


class PrivateDoctorRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrivateDoctorSerializer

    def get_object(self):
        uuid = self.request.user.uuid
        print("uuid", uuid)
        queryset = Doctor.objects.select_related("doctor_info").filter(
            doctor_info__uuid=uuid
        )
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


class PrivateDoctorProfileUpdate(CreateAPIView):
    serializer_class = PrivateDoctorSerializer
    permission_classes = [IsAuthenticated]

    # def get_object(self):
    #     # Return the current user's Doctor object
    #     return Doctor.objects.get(doctor_info=self.request.user)
