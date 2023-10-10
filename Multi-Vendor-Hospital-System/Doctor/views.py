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
    PrivateDoctorScheduleDaysConnectorSerializer,
    PrivateDoctorScheduleDateConnectorSerializer,
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
        email = self.request.user.email
        queryset = PrescriptionMedicineConnector.objects.filter(
            prescription__patient_doctor_booking__doctor_schedule_day__doctor_schedule__doctor__doctor_info__email=email
        )
        return queryset


class MedicineList(ListAPIView):
    queryset = Medicine.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MedicineSerializer

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name"]


class PrescriptionMedicalTestConnectorListCreate(ListCreateAPIView):
    serializer_class = PrescriptionMedicalTestConnectorSerializer
    permission_classes = [IsAppointmentDoctor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        prescription_uuid = self.kwargs.get("prescription_uuid")
        context["prescription_uuid"] = prescription_uuid
        return context

    def get_queryset(self):
        email = self.request.user.email
        queryset = PrescriptionMedicalTestConnector.objects.filter(
            prescription__patient_doctor_booking__doctor_schedule_day__doctor_schedule__doctor__doctor_info__email=email
        )
        return queryset


class MedicalTestList(ListAPIView):
    queryset = Medical_Test.objects.all()
    serializer_class = MedicalTestSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name"]


# ------------------ Doctor Appointments ------------------


class DoctorAppointmentsPrescriptionDetail(RetrieveAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAppointmentDoctor]

    def get_object(self):
        user_email = self.request.user.email
        uuid = self.kwargs.get("prescription_uuid")
        obj = Prescription.objects.filter(
            uuid=uuid,
            patient_doctor_booking__doctor_schedule_day__doctor_schedule__doctor__doctor_info__email=user_email,
        ).first()
        return obj


class DoctorAppointmentsPrescription(ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsAppointmentDoctor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["patient_doctor_booking"] = self.kwargs.get("appointment_uuid")
        return context

    def get_queryset(self):
        user_email = self.request.user.email
        queryset = Prescription.objects.filter(
            patient_doctor_booking__doctor_schedule_day__doctor_schedule__doctor__doctor_info__email=user_email
        )
        return queryset


class DoctorAppointmentsDetail(RetrieveAPIView):
    serializer_class = DoctorAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_email = self.request.user.email
        uuid = self.kwargs.get("appointment_uuid")
        obj = DoctorAppointment.objects.filter(
            uuid=uuid,
            doctor_schedule_day__doctor_schedule__doctor__doctor_info__email=user_email,
        ).first()

        return obj


class DoctorAppointmentsList(ListAPIView):
    serializer_class = DoctorAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = DoctorAppointment.objects.filter(
            doctor_schedule_day__doctor_schedule__doctor__doctor_info__email=self.request.user.email
        )
        return queryset


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
        context["hospital_uuid"] = self.kwargs.get("hospital_uuid")
        return context

    def get_queryset(self):
        uuid = self.kwargs.get("hospital_uuid")
        hospital = Hospital.objects.filter(uuid=uuid).first()
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
        context["hospital_uuid"] = self.kwargs.get("hospital_uuid")
        return context

    def get_queryset(self):
        uuid = self.kwargs.get("hospital_uuid")
        hospital = Hospital.objects.filter(uuid=uuid).first()
        queryset = EmergencyDoctorScedule.objects.filter(
            doctor_schedule__hospital=hospital
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
        user_email = self.request.user.email
        context = super().get_serializer_context()
        context["user_email"] = user_email
        return context

    def get_queryset(self):
        queryset = DoctorSpecialtyConnector.objects.filter(
            doctor__doctor_info__email=self.request.user.email
        )
        return queryset


# --------------- Doctor Registration ------------------


class PrivateDoctorRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrivateDoctorSerializer

    def get_object(self):
        uuid = self.request.user.uuid
        print("uuid", uuid)
        queryset = Doctor.objects.filter(doctor_info__uuid=uuid)
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


class PrivateDoctorProfileUpdate(CreateAPIView):
    serializer_class = PrivateDoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the current user's Doctor object
        return Doctor.objects.get(doctor_info=self.request.user)
