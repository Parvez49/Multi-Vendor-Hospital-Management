from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import (
    Founder,
    Hospital,
    HospitalSpecialtyConnector,
    UserHospitalRoleConnector,
)
from .permissions import IsHospitalAdmin
from .serializers import (
    PrivateFounderSerializer,
    PrivateHospitalSerializer,
    PrivateHospitalSpecialtyConnectorSerializer,
    UserHospitalRoleConnectorSerializer,
)


class UserHospitalRoleConnectorRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = UserHospitalRoleConnectorSerializer
    permission_classes = [IsHospitalAdmin]

    def get_object(self):
        uuid = self.kwargs.get("user_hospital_role_uuid")
        queryset = UserHospitalRoleConnector.objects.filter(uuid=uuid)
        obj = get_object_or_404(queryset)
        return obj


class UserHospitalRoleConnectorListCreate(ListCreateAPIView):
    # queryset = UserHospitalRoleConnector.objects.all()
    serializer_class = UserHospitalRoleConnectorSerializer
    permission_classes = [IsAuthenticated, IsHospitalAdmin]

    def get_serializer_context(self):
        # Pass the request context to the serializer
        context = super().get_serializer_context()
        context["hospital_uuid"] = self.kwargs["hospital_uuid"]
        return context

    def get_queryset(self):
        hospital_uuid = self.kwargs["hospital_uuid"]
        queryset = UserHospitalRoleConnector.objects.filter(
            hospital_user__hospital__uuid=hospital_uuid
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

    def get_permissions(self):
        if self.request.method != "POST":
            return [AllowAny()]  # Allow any for GET requests
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = Hospital.objects.all()
        return queryset
