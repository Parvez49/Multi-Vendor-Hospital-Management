from rest_framework import serializers
from Accounts.models import User
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

    def validate(self, attrs):
        user_email = self.context.get("user_email")
        doctor = Doctor.objects.filter(doctor_info__email=user_email).first()
        if not doctor:
            raise serializers.ValidationError("Doctor not found!!!")
        attrs["doctor"] = doctor.uuid
        return super().validate(attrs)

    def create(self, validated_data):
        specialty = Specialty.objects.filter(uuid=validated_data["specialty"]).first()
        if not specialty:
            raise serializers.ValidationError("Specialty not found!!!")
        doctor = Doctor.objects.filter(uuid=validated_data["doctor"]).first()
        if not doctor:
            raise serializers.ValidationError("Doctor not registered!!!")
        if (
            DoctorSpecialtyConnector.objects.filter(doctor=doctor).first()
            and DoctorSpecialtyConnector.objects.filter(specialty=specialty).first()
        ):
            raise serializers.ValidationError("Already registered!!!")
        obj = DoctorSpecialtyConnector(doctor=doctor, specialty=specialty)
        obj.save()
        return obj

    def get_doctor(self, obj):
        return obj.doctor.doctor_info.first_name


class PrivateDoctorSerializer(serializers.ModelSerializer):
    doctor_info = serializers.UUIDField()

    class Meta:
        model = Doctor
        fields = (
            "uuid",
            "doctor_info",
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
        doctor_uuid = validated_data.pop("doctor_info")
        obj = User.objects.filter(uuid=doctor_uuid).first()
        # doctor_obj = Doctor.objects.create(doctor_info=obj, **validated_data)

        doctor_obj = Doctor.objects.filter(doctor_info=obj, **validated_data).first()
        if not doctor_obj:
            doctor_obj = Doctor.objects.create(doctor_info=obj, **validated_data)
            doctor_obj.save()
        return doctor_obj
