from django.contrib import admin

# Register your models here.

from .models import (
    Hospital,
    Founder,
    HospitalSpecialtyConnector,
    UserHospitalRole,
    UserHospitalRoleConnector,
)


class HospitalSpecialtyConnectorAttr(admin.ModelAdmin):
    list_display = ["uuid", "hospital", "specialty"]


admin.site.register(HospitalSpecialtyConnector, HospitalSpecialtyConnectorAttr)


class HospitalAttr(admin.ModelAdmin):
    list_display = ["uuid", "registration_no", "hospital_name", "logo", "city"]


admin.site.register(Hospital, HospitalAttr)


class FounderAttr(admin.ModelAdmin):
    list_display = ["founder", "hospital"]


admin.site.register(Founder, FounderAttr)


class UserHospitalRoleAttr(admin.ModelAdmin):
    list_display = ["uuid", "user", "hospital"]


admin.site.register(UserHospitalRole, UserHospitalRoleAttr)


class UserHospitalRoleAttr(admin.ModelAdmin):
    list_display = ["uuid", "hospital_user", "role"]


admin.site.register(UserHospitalRoleConnector, UserHospitalRoleAttr)
