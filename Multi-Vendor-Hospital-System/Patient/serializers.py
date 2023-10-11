from rest_framework import serializers

from datetime import datetime

from Accounts.models import User
from Doctor.models import Doctor
from Accounts.permissions import authenticateUser
from Common.models import Medical_Test, Medicine
from Common.serializers import HospitalListSlimSerializer, PatientSlimSerializer

from Hospital.models import Hospital, UserHospitalRoleConnector
from .models import (
    DoctorAppointment,
    DoctorScheduleDaysConnector,
    Prescription,
    PrescriptionMedicalTestConnector,
    PrescriptionMedicineConnector,
)
from .tasks import send_appointment_reminders
from datetime import timedelta


class PrescriptionSerializer(serializers.ModelSerializer):
    # patient_doctor_booking = serializers.UUIDField()  # Doctor Booking table
    patient = serializers.SerializerMethodField()
    medical_tests = serializers.SerializerMethodField()
    medicines = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = (
            "uuid",
            # "patient_doctor_booking",
            "patient",
            "prescription_date",
            "previous_medications",
            "diagnosis",
            "special_instructions",
            "medical_tests",
            "medicines",
        )

    def validate(self, attrs):
        patient_doctor_booking = DoctorAppointment.objects.filter(
            uuid=self.context.get("patient_doctor_booking")
        ).first()
        attrs["patient_doctor_booking"] = patient_doctor_booking
        return super().validate(attrs)

    def get_patient(self, obj):
        date_of_birth = str(obj.patient_doctor_booking.patient.date_of_birth)
        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
        current_date = datetime.now()
        age = current_date.year - date_of_birth.year
        patient_data = {
            "patient": f"{obj.patient_doctor_booking.patient.first_name} {obj.patient_doctor_booking.patient.last_name}",
            "age": age,
        }
        return patient_data

    def get_medical_tests(self, obj):
        # Get the list of medical tests associated with the prescription
        medical_tests = PrescriptionMedicalTestConnector.objects.filter(
            prescription=obj
        )
        return [medical_test.test.name for medical_test in medical_tests]

    def get_medicines(self, obj):
        # Get the list of medicines associated with the prescription
        medicines = PrescriptionMedicineConnector.objects.filter(prescription=obj)
        return [medicine.medicine.name for medicine in medicines]


class PrescriptionMedicalTestConnectorSerializer(serializers.ModelSerializer):
    # prescription = PrescriptionSerializer()
    test = serializers.UUIDField()

    class Meta:
        model = PrescriptionMedicalTestConnector
        fields = ["uuid", "test"]

    def validate(self, attrs):
        prescription_uuid = self.context.get("prescription_uuid")
        prescription_obj = Prescription.objects.filter(uuid=prescription_uuid).first()
        if not prescription_obj:
            raise serializers.ValidationError("Wrong Prescription uuid!!!")

        attrs["prescription"] = prescription_obj
        return super().validate(attrs)

    def create(self, validated_data):
        test = Medical_Test.objects.filter(uuid=validated_data["test"]).first()
        if not test:
            raise serializers.ValidationError("Medical Test not found!!!")
        validated_data["test"] = test

        medical_test = PrescriptionMedicalTestConnector.objects.filter(
            **validated_data
        ).first()
        if not medical_test:
            medical_test = PrescriptionMedicalTestConnector.objects.create(
                **validated_data
            )
            medical_test.save()
        return medical_test


class PrescriptionMedicineConnectorSerializer(serializers.ModelSerializer):
    medicine = serializers.UUIDField()

    class Meta:
        model = PrescriptionMedicineConnector
        fields = ("uuid", "medicine")

    def validate(self, attrs):
        prescription_uuid = self.context.get("prescription_uuid")
        prescription_obj = Prescription.objects.filter(uuid=prescription_uuid).first()
        if not prescription_obj:
            raise serializers.ValidationError("Wrong Prescription uuid!!!")
        attrs["prescription"] = prescription_obj
        return super().validate(attrs)

    def create(self, validated_data):
        medicine = Medicine.objects.filter(uuid=validated_data["medicine"]).first()
        if not medicine:
            raise serializers.ValidationError("Medicine not found!!!")
        validated_data["medicine"] = medicine
        medicine_obj = PrescriptionMedicineConnector.objects.filter(
            **validated_data
        ).first()
        if not medicine_obj:
            medicine_obj = PrescriptionMedicineConnector.objects.create(
                **validated_data
            )
            medicine_obj.save()
        return medicine_obj


class DoctorAppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSlimSerializer(read_only=True)
    hospital = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    serial_no = serializers.SerializerMethodField()
    doctor_schedule_day = serializers.UUIDField(write_only=True)

    class Meta:
        model = DoctorAppointment
        fields = (
            "uuid",
            "serial_no",
            "doctor_schedule_day",
            "hospital",
            "patient",
            "doctor",
            "date",
        )

    def get_serial_no(self, obj):
        return obj.serial_no

    def get_hospital(self, obj):
        hospital_data = {
            "hospital_name": obj.doctor_schedule_day.doctor_schedule.hospital.hospital_name,
            "description": obj.doctor_schedule_day.doctor_schedule.hospital.description,
            "city": obj.doctor_schedule_day.doctor_schedule.hospital.city,
        }
        return hospital_data

    def get_doctor(self, obj):
        doctor_data = {
            "uuid": obj.uuid,
            "name": f"{obj.doctor_schedule_day.doctor_schedule.doctor.doctor_info.first_name} {obj.doctor_schedule_day.doctor_schedule.doctor.doctor_info.last_name}",
            "department": obj.doctor_schedule_day.doctor_schedule.doctor.department,
            "degrees": obj.doctor_schedule_day.doctor_schedule.doctor.degrees,
        }
        return doctor_data

    def validate(self, attrs):
        request = self.context.get("request")
        patient = request.user
        attrs["patient"] = patient

        doctor_schedule_day = DoctorScheduleDaysConnector.objects.filter(
            uuid=attrs["doctor_schedule_day"]
        ).first()
        if doctor_schedule_day:
            if doctor_schedule_day.day.day != attrs["date"].strftime("%A"):
                raise serializers.ValidationError("Invalid Date")

        # Check if the maximum patient limit is reached for this schedule and date
        existing_appointments_count = DoctorAppointment.objects.filter(
            doctor_schedule_day=doctor_schedule_day, date=attrs["date"]
        ).count()

        if (
            existing_appointments_count
            >= doctor_schedule_day.doctor_schedule.maximum_patient
        ):
            raise serializers.ValidationError(
                "Maximum patient limit reached for this schedule and date."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        doctor_schedule_day = DoctorScheduleDaysConnector.objects.filter(
            uuid=validated_data["doctor_schedule_day"]
        ).first()
        if not doctor_schedule_day:
            raise serializers.ValidationError("Invalid schedule!!!")

        validated_data["doctor_schedule_day"] = doctor_schedule_day

        obj = DoctorAppointment.objects.filter(**validated_data).first()

        if not obj:
            date = validated_data["date"]
            serial_no = DoctorAppointment.objects.filter(date=date).count() + 1
            validated_data["serial_no"] = serial_no
            obj = DoctorAppointment.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("You already booked this appointment")

        return obj


class HospitalDoctorScheduleAppointmentSerializer(serializers.ModelSerializer):
    appointment = serializers.SerializerMethodField()

    class Meta:
        model = DoctorAppointment
        fields = ("appointment",)

    def get_appointment(self, obj):
        data = {
            "patient": obj.patient.first_name + " " + obj.patient.last_name,
            "start_time": obj.doctor_schedule_day.doctor_schedule.start_time,
            "end_time": obj.doctor_schedule_day.doctor_schedule.end_time,
            "date": obj.date,
        }
        return data


class PrescriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ("uuid", "prescription_date")


class PatientPrescriptionDetailSerializer(serializers.ModelSerializer):
    medical_tests = serializers.SerializerMethodField()
    medicines = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = (
            "prescription_date",
            "previous_medications",
            "diagnosis",
            "special_instructions",
            "medical_tests",
            "medicines",
        )

    def get_medical_tests(self, obj):
        # Get the list of medical tests associated with the prescription
        medical_tests = PrescriptionMedicalTestConnector.objects.filter(
            prescription=obj
        )
        return [medical_test.test.name for medical_test in medical_tests]

    def get_medicines(self, obj):
        # Get the list of medicines associated with the prescription
        medicines = PrescriptionMedicineConnector.objects.filter(prescription=obj)
        return [medicine.medicine.name for medicine in medicines]


class DoctorAppointmentUpdateDeleteSerializer(serializers.ModelSerializer):
    doctor_schedule_day = serializers.UUIDField()
    patient = serializers.UUIDField()

    class Meta:
        model = DoctorAppointment
        fields = ("uuid", "doctor_schedule_day", "patient", "date")

    def validate(self, attrs):
        request = self.context.get("request")
        patient = User.objects.get(uuid=attrs["patient"])
        attrs["patient"] = patient

        doctor_schedule_day = DoctorScheduleDaysConnector.objects.filter(
            uuid=attrs["doctor_schedule_day"]
        ).first()
        if doctor_schedule_day:
            if doctor_schedule_day.day.day != attrs["date"].strftime("%A"):
                raise serializers.ValidationError("Invalid Date")
        attrs["doctor_schedule_day"] = doctor_schedule_day

        return super().validate(attrs)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
