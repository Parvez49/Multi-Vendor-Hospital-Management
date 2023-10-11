from rest_framework import serializers
from Accounts.models import User
from Hospital.models import Hospital
from Common.models import Days, HospitalRole, Specialty
from Doctor.models import (
    Doctor,
    DoctorSchedule,
    DoctorScheduleDaysConnector,
    EmergencyDoctorScedule,
)
from .models import (
    Hospital,
    Founder,
    UserHospitalRole,
    UserHospitalRoleConnector,
)


from rest_framework import serializers
from .models import HospitalSpecialtyConnector


class PrivateDoctorScheduleSerializer(serializers.ModelSerializer):
    doctor = serializers.UUIDField()
    hospital = serializers.SerializerMethodField()

    class Meta:
        model = DoctorSchedule
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

        hospital_slug = self.context["hospital_slug"]
        hospital_obj = Hospital.objects.filter(slug=hospital_slug).first()

        if not hospital_obj:
            raise serializers.ValidationError("Hospital not found!!!")

        doctor_schedule_data["hospital"] = hospital_obj

        # Check if a DoctorSchedule with the same doctor and hospital already exists
        doctor_schedule, created = DoctorSchedule.objects.get_or_create(
            doctor=doctor_obj, **doctor_schedule_data
        )

        days_connector, created = DoctorScheduleDaysConnector.objects.get_or_create(
            doctor_schedule=doctor_schedule, **validated_data
        )
        return days_connector


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
            slug=self.context["hospital_slug"]
        ).first()
        if not hospital_obj:
            raise serializers.ValidationError("Hospital not found!!!")

        doctor_schedule_data["hospital"] = hospital_obj

        # Check if a DoctorSchedule with the same doctor and hospital already exists
        doctor_schedule, created = DoctorSchedule.objects.get_or_create(
            doctor=doctor_obj, **doctor_schedule_data
        )
        date_connector, created = EmergencyDoctorScedule.objects.get_or_create(
            doctor_schedule=doctor_schedule, **validated_data
        )
        return date_connector


class HospitalDoctorScheduleSerializer(serializers.ModelSerializer):
    schedule = serializers.SerializerMethodField()
    hospital = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = DoctorScheduleDaysConnector
        fields = ("hospital", "doctor", "schedule")

    def get_schedule(self, obj):
        doctor_schedule = obj.doctor_schedule
        data = {
            "uuid": obj.uuid,
            "start_time": doctor_schedule.start_time,
            "end_time": doctor_schedule.end_time,
            "day": obj.day.day,
        }
        return data

    def get_hospital(self, obj):
        return obj.doctor_schedule.hospital.hospital_name

    def get_doctor(self, obj):
        return (
            obj.doctor_schedule.doctor.doctor_info.first_name
            + " "
            + obj.doctor_schedule.doctor.doctor_info.last_name
        )


class HospitalDoctorListSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    hospital = serializers.SerializerMethodField()

    class Meta:
        model = UserHospitalRoleConnector
        fields = ("hospital", "doctor")

    def get_doctor(self, obj):
        user = obj.hospital_user.user
        doctor_obj = Doctor.objects.filter(doctor_info=user).first()
        user_data = {
            "uuid": doctor_obj.uuid,
            "name": f"{user.first_name} {user.last_name}",
            "slug": doctor_obj.slug,
            "department": doctor_obj.department,
            "degrees": doctor_obj.degrees,
        }
        return user_data

    def get_hospital(self, obj):
        hospital_data = {
            "hospital_name": obj.hospital_user.hospital.hospital_name,
            "description": obj.hospital_user.hospital.description,
            "city": obj.hospital_user.hospital.city,
        }
        return hospital_data


class UserHospitalRoleSerializer(serializers.ModelSerializer):
    user = serializers.EmailField()
    hospital = serializers.SerializerMethodField()

    class Meta:
        model = UserHospitalRole
        fields = ["user", "hospital"]

    def validate(self, attrs):
        hospital_uuid = self.context.get("hospital_uuid")
        attrs["hospital"] = hospital_uuid
        return super().validate(attrs)

    def get_hospital(self, obj):
        return obj.hospital.hospital_name


class UserHospitalRoleConnectorSerializer(serializers.ModelSerializer):
    hospital_user = UserHospitalRoleSerializer()
    role = serializers.UUIDField()

    class Meta:
        model = UserHospitalRoleConnector
        fields = ("uuid", "hospital_user", "role")

    def create(self, validated_data):
        hospital_user_data = validated_data.pop("hospital_user")
        user = User.objects.filter(email=hospital_user_data["user"]).first()
        if not user:
            raise serializers.ValidationError("User not registered!!!")
        hospital_user_data["user"] = user
        hospital = Hospital.objects.filter(uuid=hospital_user_data["hospital"]).first()
        if not hospital:
            raise serializers.ValidationError("Hospital not found!!!")
        hospital_user = UserHospitalRole.objects.filter(
            user=user, hospital=hospital
        ).first()
        if not hospital_user:
            hospital_user = UserHospitalRole.objects.create(
                user=user, hospital=hospital
            )
        role = HospitalRole.objects.filter(uuid=validated_data["role"]).first()
        if not role:
            raise serializers.ValidationError("Invalid role uuid!!!")

        obj = UserHospitalRoleConnector.objects.filter(
            hospital_user=hospital_user, role=role
        ).first()
        if not obj:
            obj = UserHospitalRoleConnector.objects.create(
                hospital_user=hospital_user, role=role
            )
        return obj


class PrivateHospitalSpecialtyConnectorSerializer(serializers.ModelSerializer):
    hospital = serializers.UUIDField()
    specialty = serializers.UUIDField()

    class Meta:
        model = HospitalSpecialtyConnector
        fields = ("uuid", "hospital", "specialty")

    def create(self, validated_data):
        specialty = Specialty.objects.filter(uuid=validated_data["specialty"]).first()
        if not specialty:
            raise serializers.ValidationError("Specialty not found!!!")
        hospital = Hospital.objects.filter(uuid=validated_data["hospital"]).first()
        if not hospital:
            raise serializers.ValidationError("Hospital not registered!!!")
        if (
            HospitalSpecialtyConnector.objects.filter(hospital=hospital).first()
            and HospitalSpecialtyConnector.objects.filter(specialty=specialty).first()
        ):
            raise serializers.ValidationError("Already registered!!!")
        obj = HospitalSpecialtyConnector(hospital=hospital, specialty=specialty)
        obj.save()
        return obj


class PrivateFounderSerializer(serializers.ModelSerializer):
    founder = serializers.UUIDField()
    hospital = serializers.UUIDField()

    class Meta:
        model = Founder
        fields = ("founder", "hospital")

    def create(self, validated_data):
        user = User.objects.filter(uuid=validated_data["founder"]).first()
        if not user:
            raise serializers.ValidationError("User not registered!!!")
        hospital = Hospital.objects.filter(uuid=validated_data["hospital"]).first()
        if not hospital:
            raise serializers.ValidationError("Hospital not registered!!!")
        if (
            Founder.objects.filter(founder=user).first()
            and Founder.objects.filter(hospital=hospital).first()
        ):
            raise serializers.ValidationError("Already registered!!!")
        founder = Founder.objects.create(founder=user, hospital=hospital)
        founder.save()

        # The founder are automatically admin of his Hospital
        role = HospitalRole.objects.filter(role="Admin").first()
        if not role:
            role = HospitalRole.objects.create(role="Admin")
        hospital_user = UserHospitalRole.objects.filter(
            user=user, hospital=hospital
        ).first()
        if not hospital_user:
            hospital_user = UserHospitalRole.objects.create(
                user=user, hospital=hospital
            )

        obj = UserHospitalRoleConnector(hospital_user=hospital_user, role=role)
        obj.save()

        return founder


class PhoneNumberSerializerField(serializers.CharField):
    def to_representation(self, obj):
        return str(obj)

    def to_internal_value(self, data):
        return data


class PrivateHospitalSerializer(serializers.ModelSerializer):
    contact_number = PhoneNumberSerializerField()
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Hospital
        fields = (
            "uuid",
            "slug",
            "registration_no",
            "hospital_name",
            "city",
            "state",
            "postal_code",
            "country",
            "contact_number",
            "website",
            "description",
            "additional_notes",
            "operating_hours",
            "insurance_accepted",
            "facilities",
            "logo",
        )

    def get_slug(self, obj):
        return obj.slug
