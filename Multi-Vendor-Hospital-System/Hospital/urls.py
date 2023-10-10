from django.urls import path
from . import views

urlpatterns = [
    # ------------- User Hospital Role -------------------
    path(
        "/<uuid:hospital_uuid>/user/roles/<uuid:user_hospital_role_uuid>",
        views.UserHospitalRoleConnectorRetrieveUpdateDestroy.as_view(),
        name="user-hospital-role-detail",
    ),
    path(
        "/<uuid:hospital_uuid>/user/roles",
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
    # ------------ Hospital -----------------
    path(
        "/<uuid:hospital_uuid>",
        views.PrivateHospitalRetrieveUpdateDestroy.as_view(),
        name="hospital-detail",
    ),
    path(
        "/register",
        views.PrivateHospitalListCreate.as_view(),
        name="hospital-list-create",
    ),
]
