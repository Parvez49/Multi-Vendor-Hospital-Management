from rest_framework import serializers

from Accounts.models import User
from Accounts.serializers import PublicUserSerializer
from Common.models import Specialty, Medical_Test, Medicine
from Hospital.models import Hospital
from Patient.models import DoctorAppointment
from .models import (
    EmergencyDoctorScedule,
    Doctor,
    DoctorSpecialtyConnector,
    DoctorSchedule,
    DoctorScheduleDaysConnector,
)


from Common.models import Days


class PrivateDoctorSpecialtyConnectorSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    specialty = serializers.UUIDField()

    class Meta:
        model = DoctorSpecialtyConnector
        fields = ["uuid", "doctor", "specialty"]

    def create(self, validated_data):
        specialty = Specialty.objects.filter(uuid=validated_data["specialty"]).first()
        if not specialty:
            raise serializers.ValidationError("Specialty not found!!!")

        user = self.context.get("user")
        doctor = Doctor.objects.filter(doctor_info=user).first()
        if not doctor:
            raise serializers.ValidationError("Doctor not registered!!!")

        obj = DoctorSpecialtyConnector(doctor=doctor, specialty=specialty)
        obj.save()
        return obj

    def get_doctor(self, obj):
        return obj.doctor.doctor_info.first_name


class PrivateDoctorSerializer(serializers.ModelSerializer):
    doctor_data = serializers.UUIDField(write_only=True)
    doctor_info = PublicUserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = (
            "uuid",
            "doctor_info",
            "doctor_data",
            "department",
            "designation",
            "degrees",
            "medical_school",
            "license_number",
            "license_expiry_date",
            "emergency_contact",
            "languages_spoken",
            "notes",
        )

    def create(self, validated_data):
        doctor_uuid = validated_data.pop("doctor_data")
        obj = User.objects.filter(uuid=doctor_uuid).first()
        doctor_obj, _ = Doctor.objects.select_related("doctor_info").get_or_create(
            doctor_info=obj, **validated_data
        )

        return doctor_obj
