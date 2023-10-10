from rest_framework import serializers
from Accounts.models import User
from Hospital.models import Hospital
from Common.models import HospitalRole, Specialty
from .models import (
    Hospital,
    Founder,
    UserHospitalRole,
    UserHospitalRoleConnector,
)


from rest_framework import serializers
from .models import HospitalSpecialtyConnector


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

    class Meta:
        model = Hospital
        fields = (
            "uuid",
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
