from django.urls import path
from . import views

urlpatterns = [
    path(
        "/<slug:hospital_slug>/schedules/days/<uuid:schedule_uuid>",
        views.PrivateDoctorScheduleDaysConnectorRetrieveUpdateDestroy.as_view(),
        name="doctor-schedule-with-day-details",
    ),
    path(
        "/<slug:hospital_slug>/schedules/days",
        views.PrivateDoctorScheduleDaysConnectorListCreate.as_view(),
        name="create-doctor-schedule-with-day",
    ),
    path(
        "/<slug:hospital_slug>/schedules/date/<uuid:schedule_uuid>",
        views.PrivateDoctorScheduleDateConnectorRetrieveUpdateDestroy.as_view(),
        name="doctor-schedule-with-date-details",
    ),
    path(
        "/<slug:hospital_slug>/schedules/date",
        views.PrivateDoctorScheduleDateConnectorListCreate.as_view(),
        name="create-doctor-schedule-with-date",
    ),
    path(
        "/<slug:hospital_slug>/doctors/<slug:doctor_slug>/schedules",
        views.HospitalDoctorSchedule.as_view(),
        name="hospital-doctor-schedule-list",
    ),
    path(
        "/<slug:hospital_slug>/doctors",
        views.HospitalDoctorList.as_view(),
        name="hospital-doctor-list",
    ),
    # ------------- User Hospital Role -------------------
    path(
        "/<slug:hospital_slug>/user/roles/<uuid:user_hospital_role_uuid>",
        views.UserHospitalRoleConnectorRetrieveUpdateDestroy.as_view(),
        name="user-hospital-role-detail",
    ),
    path(
        "/<slug:hospital_slug>/user/roles",
        views.UserHospitalRoleConnectorListCreate.as_view(),
        name="user-hospital-role-create",
    ),
    # --------------- Hospital Specialty ----------------
    path(
        "/specialties/<uuid:specialty_uuid>",
        views.PrivateHospitalSpecialtyConnectorRetrieveUpdateDestroy.as_view(),
        name="hospital-specialty-connector-detail",
    ),
    path(
        "/specialties",
        views.PrivateHospitalSpecialtyConnectorListCreate.as_view(),
        name="hospital-specialty-connector-list-create",
    ),
    # ------------ Founder -----------------
    path(
        "/founders/<uuid:founder_uuid>",
        views.PrivateFounderRetrieveUpdateDestroy.as_view(),
        name="founder-detail",
    ),
    path(
        "/founders",
        views.PrivateFounderListCreate.as_view(),
        name="founder-list-create",
    ),
    path(
        "/<slug:hospital_slug>",
        views.PrivateHospitalRetrieveUpdateDestroy.as_view(),
        name="hospital-detail",
    ),
    path(
        "",
        views.PrivateHospitalListCreate.as_view(),
        name="hospital-list-create",
    ),
]
