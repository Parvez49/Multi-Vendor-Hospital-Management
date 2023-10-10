from django.contrib import admin

# Register your models here.


from .models import (
    DoctorAppointment,
    Prescription,
    PrescriptionMedicalTestConnector,
    PrescriptionMedicineConnector,
)


class PrescriptionAttr(admin.ModelAdmin):
    list_display = [
        "uuid",
        "patient_doctor_booking",
        "prescription_date",
        "previous_medications",
        "diagnosis",
    ]


admin.site.register(Prescription, PrescriptionAttr)


class PrescriptionMedicalTestConnectorAttr(admin.ModelAdmin):
    list_display = ["uuid", "prescription", "test"]


admin.site.register(
    PrescriptionMedicalTestConnector, PrescriptionMedicalTestConnectorAttr
)


class PrescriptionMedicineConnectorAttr(admin.ModelAdmin):
    list_display = ["uuid", "prescription", "medicine"]


admin.site.register(PrescriptionMedicineConnector)


class DoctorAppointmentAttr(admin.ModelAdmin):
    list_display = ["uuid", "doctor_schedule_day", "patient", "date"]


admin.site.register(DoctorAppointment, DoctorAppointmentAttr)
