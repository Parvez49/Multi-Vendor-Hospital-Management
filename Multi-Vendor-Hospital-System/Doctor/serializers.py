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


class PrivateDoctorScheduleSerializer(serializers.ModelSerializer):
    doctor = serializers.UUIDField()
    hospital = serializers.SerializerMethodField()

    class Meta:
        model = DoctorSchedule
        # fields = "__all__"
        fields = (
            "uuid",
            "doctor",
            "hospital",
            "start_time",
            "end_time",
            "activity_type",
            "maximum_patient",
        )

    def validate(self, attrs):
        hospital_uuid = self.context.get("hospital_uuid")
        attrs["hospital"] = hospital_uuid
        return super().validate(attrs)

    def get_hospital(self, obj):
        return obj.hospital.hospital_name


class PrivateDoctorScheduleDateConnectorSerializer(serializers.ModelSerializer):
    doctor_schedule = PrivateDoctorScheduleSerializer()

    class Meta:
        model = EmergencyDoctorScedule
        fields = ("uuid", "doctor_schedule", "schedule_date")

    def create(self, validated_data):
        doctor_schedule_data = validated_data.pop("doctor_schedule")
        doctor_obj = Doctor.objects.filter(
            uuid=doctor_schedule_data.pop("doctor")
        ).first()
        if not doctor_obj:
            raise serializers.ValidationError("Doctor not registered!!!")
        hospital_obj = Hospital.objects.filter(
            uuid=doctor_schedule_data.pop("hospital")
        ).first()
        if not hospital_obj:
            raise serializers.ValidationError("Hospital not found!!!")

        # Check if a DoctorSchedule with the same doctor and hospital already exists
        doctor_schedule = DoctorSchedule.objects.filter(
            doctor=doctor_obj, hospital=hospital_obj, **doctor_schedule_data
        ).first()
        if not doctor_schedule:
            doctor_schedule = DoctorSchedule.objects.create(
                doctor=doctor_obj, hospital=hospital_obj, **doctor_schedule_data
            )
            doctor_schedule.save()
        date_connector = EmergencyDoctorScedule.objects.filter(
            doctor_schedule=doctor_schedule, **validated_data
        ).first()
        if not date_connector:
            date_connector = EmergencyDoctorScedule.objects.create(
                doctor_schedule=doctor_schedule, **validated_data
            )
            date_connector.save()
        return date_connector


from Common.models import Days


class PrivateDoctorScheduleDaysConnectorSerializer(serializers.ModelSerializer):
    doctor_schedule = PrivateDoctorScheduleSerializer()
    day = serializers.UUIDField()

    class Meta:
        model = DoctorScheduleDaysConnector
        fields = ("uuid", "doctor_schedule", "day")

    def validate(self, attrs):
        day = Days.objects.filter(uuid=attrs["day"]).first()
        if not day:
            raise serializers.ValidationError("Invalid Day uuid")
        attrs["day"] = day
        return super().validate(attrs)

    def create(self, validated_data):
        doctor_schedule_data = validated_data.pop("doctor_schedule")
        doctor_obj = Doctor.objects.filter(
            uuid=doctor_schedule_data.pop("doctor")
        ).first()
        if not doctor_obj:
            raise serializers.ValidationError("Doctor not registered!!!")
        hospital_obj = Hospital.objects.filter(
            uuid=doctor_schedule_data.pop("hospital")
        ).first()
        if not hospital_obj:
            raise serializers.ValidationError("Hospital not found!!!")

        # Check if a DoctorSchedule with the same doctor and hospital already exists
        doctor_schedule = DoctorSchedule.objects.filter(
            doctor=doctor_obj, hospital=hospital_obj, **doctor_schedule_data
        ).first()
        if not doctor_schedule:
            doctor_schedule = DoctorSchedule.objects.create(
                doctor=doctor_obj, hospital=hospital_obj, **doctor_schedule_data
            )
            doctor_schedule.save()
        days_connector = DoctorScheduleDaysConnector.objects.filter(
            doctor_schedule=doctor_schedule, **validated_data
        ).first()
        if not days_connector:
            days_connector = DoctorScheduleDaysConnector.objects.create(
                doctor_schedule=doctor_schedule, **validated_data
            )
            days_connector.save()
        return days_connector


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
