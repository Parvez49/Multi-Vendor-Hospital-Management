from django.contrib import admin

# Register your models here.

from .models import Days, HospitalRole, Specialty, Medical_Test, Medicine


class DaysAttr(admin.ModelAdmin):
    list_display = ["uuid", "day"]


admin.site.register(Days, DaysAttr)


class HospitalRoleAttr(admin.ModelAdmin):
    list_display = ["uuid", "role"]


admin.site.register(HospitalRole, HospitalRoleAttr)


class SpecialtyAttr(admin.ModelAdmin):
    list_display = ["uuid", "specialty"]


admin.site.register(Specialty, SpecialtyAttr)


class MedicineAttr(admin.ModelAdmin):
    list_display = [
        "uuid",
        "name",
        "dosage",
        "duration",
        "morning",
        "noon",
        "evening",
        "price",
    ]


admin.site.register(Medicine, MedicineAttr)


class Medical_TestAttr(admin.ModelAdmin):
    list_display = ["uuid", "name", "process", "price"]


admin.site.register(Medical_Test, Medical_TestAttr)
