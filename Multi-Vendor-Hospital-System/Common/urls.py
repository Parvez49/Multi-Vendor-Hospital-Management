from django.urls import path
from . import views

urlpatterns = [
    path(
        "/days/<uuid:day_uuid>",
        views.PrivateDaysRetrieveUpdate.as_view(),
        name="day-detail",
    ),
    path(
        "/days",
        views.PrivateDaysListCreate.as_view(),
        name="days-list-create",
    ),
    # ------------- Hospital Role --------------------
    path(
        "/hospital/roles/<uuid:role_uuid>",
        views.HospitalRoleRetrieveUpdateDestroy.as_view(),
        name="hospital-role-detail",
    ),
    path(
        "/hospital/roles",
        views.HospitalRoleListCreate.as_view(),
        name="hospital-role-list-create",
    ),
    # ------------ Specialty ----------------
    path(
        "/specialties/<uuid:specialty_uuid>",
        views.PrivateSpecialtyRetrieveUpdateDestroy.as_view(),
        name="specialty-detail",
    ),
    path(
        "/specialties",
        views.PrivateSpecialtyListCreate.as_view(),
        name="specialty-list-create",
    ),
    path(
        "/medical/tests/<uuid:test_uuid>",
        views.MedicalTestRetrieveUpdateDestroy.as_view(),
        name="medical-test-detail",
    ),
    path(
        "/medical/tests",
        views.MedicalTestListCreate.as_view(),
        name="medical-test-list-create",
    ),
    path(
        "/medicines/<uuid:medicine_uuid>",
        views.MedicineRetrieveUpdate.as_view(),
        name="medicine-detail",
    ),
    path(
        "/medicines",
        views.MedicineListCreate.as_view(),
        name="medicine-list-create",
    ),
]
