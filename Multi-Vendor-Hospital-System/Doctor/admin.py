from django.contrib import admin

# Register your models here.

from .models import (
    Doctor,
    DoctorSpecialtyConnector,
    DoctorSchedule,
    DoctorScheduleDaysConnector,
    EmergencyDoctorScedule,
)


class DoctorAttr(admin.ModelAdmin):
    list_display = ["uuid", "doctor_info"]


admin.site.register(Doctor, DoctorAttr)


class DoctorSpecialtyConnectorAttr(admin.ModelAdmin):
    list_display = ["uuid", "doctor", "specialty"]


admin.site.register(DoctorSpecialtyConnector, DoctorSpecialtyConnectorAttr)


class DoctorScheduleAttr(admin.ModelAdmin):
    list_display = [
        "uuid",
        "doctor",
        "hospital",
        "start_time",
        "end_time",
        "activity_type",
        "maximum_patient",
    ]


admin.site.register(DoctorSchedule, DoctorScheduleAttr)


class DoctorScheduleDaysConnectorAttr(admin.ModelAdmin):
    list_display = ["uuid", "doctor_schedule", "day"]


admin.site.register(DoctorScheduleDaysConnector, DoctorScheduleDaysConnectorAttr)


class EmergencyDoctorSceduleAttr(admin.ModelAdmin):
    list_display = ["uuid", "doctor_schedule", "schedule_date"]


admin.site.register(EmergencyDoctorScedule, EmergencyDoctorSceduleAttr)
