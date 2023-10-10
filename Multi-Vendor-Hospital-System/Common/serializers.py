from rest_framework import serializers

from Accounts.models import User
from Hospital.models import Hospital
from .models import Days, Specialty, HospitalRole, Medicine, Medical_Test


class PrivateDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Days
        fields = ("uuid", "day")


class PrivateSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("uuid", "specialty")


class HospitalRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalRole
        fields = ("uuid", "role")


class MedicalTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical_Test
        fields = (
            "uuid",
            "name",
            "process",
            "price",
        )

    def create(self, validated_data):
        obj = Medical_Test.objects.filter(**validated_data).first()
        if not obj:
            obj = Medical_Test.objects.create(**validated_data)
            obj.save()
        return obj


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = (
            "uuid",
            "name",
            "dosage",
            "duration",
            "method_of_taken",
            "morning",
            "noon",
            "evening",
            "price",
        )

    def create(self, validated_data):
        obj = Medicine.objects.filter(**validated_data).first()
        if not obj:
            obj = Medicine.objects.create(**validated_data)
            obj.save()
        return obj


class HospitalListSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ("uuid", "hospital_name", "description", "city")


class PatientSlimSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("uuid", "name", "email")

    def get_name(self, obj):
        return obj.first_name + " " + obj.last_name
