from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Days, HospitalRole, Specialty, Medicine, Medical_Test
from .serializers import (
    PrivateDaysSerializer,
    PrivateSpecialtySerializer,
    HospitalRoleSerializer,
    MedicalTestSerializer,
    MedicineSerializer,
)


#   ---------------- Days --------------------------


class PrivateDaysRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = PrivateDaysSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        uuid = self.kwargs.get("day_uuid")
        queryset = Days.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        return obj


class PrivateDaysListCreate(ListCreateAPIView):
    queryset = Days.objects.all()
    serializer_class = PrivateDaysSerializer
    permission_classes = [IsAdminUser]


# --------------- Hospital Role ---------------------------


class HospitalRoleRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = HospitalRoleSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        uuid = self.kwargs.get("role_uuid")
        queryset = HospitalRole.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        return obj


class HospitalRoleListCreate(ListCreateAPIView):
    queryset = HospitalRole.objects.all()
    serializer_class = HospitalRoleSerializer
    permission_classes = [IsAdminUser]


# ------------------Specialty-----------------------


class PrivateSpecialtyRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateSpecialtySerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        uuid = self.kwargs.get("specialty_uuid")
        queryset = Specialty.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        return obj


class PrivateSpecialtyListCreate(ListCreateAPIView):
    queryset = Specialty.objects.all()
    serializer_class = PrivateSpecialtySerializer
    permission_classes = [IsAdminUser]


# ------------Medical Test -----------------


class MedicalTestRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = MedicalTestSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        uuid = self.kwargs.get("test_uuid")
        queryset = Medical_Test.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        return obj


class MedicalTestListCreate(ListCreateAPIView):
    queryset = Medical_Test.objects.all()
    serializer_class = MedicalTestSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]  # Allow any for GET requests
        return [IsAdminUser()]


# ------------- Medicine --------------


class MedicineRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = MedicineSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        uuid = self.kwargs.get("medicine_uuid")
        queryset = Medicine.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        return obj


class MedicineListCreate(ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]  # Allow any for GET requests
        return [IsAdminUser()]
