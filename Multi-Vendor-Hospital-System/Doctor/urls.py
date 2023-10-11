from django.urls import path
from . import views

urlpatterns = [
    # -------------------- Doctor Appointments -----------------------
    path(
        "/appointments/<uuid:appointment_uuid>/prescriptions/<uuid:prescription_uuid>/medicines",
        views.PrescriptionMedicineConnectorListCreate.as_view(),
        name="doctor-appointments-Prescription-medicine",
    ),
    path(
        "/appointments/<uuid:appointment_uuid>/prescriptions/<uuid:prescription_uuid>/medical/tests",
        views.PrescriptionMedicalTestConnectorListCreate.as_view(),
        name="doctor-appointments-Prescription-medical-test",
    ),
    path(
        "/appointments/<uuid:appointment_uuid>/prescriptions/<uuid:prescription_uuid>",
        views.DoctorAppointmentsPrescriptionDetail.as_view(),
        name="doctor-appointments-Prescription-detail",
    ),
    path(
        "/appointments/<uuid:appointment_uuid>/prescriptions",
        views.DoctorAppointmentsPrescription.as_view(),
        name="doctor-appointments-Prescription",
    ),
    path(
        "/appointments/<uuid:appointment_uuid>",
        views.DoctorAppointmentsDetail.as_view(),
        name="doctor-appointments-Detail",
    ),
    path(
        "/appointments",
        views.DoctorAppointmentsList.as_view(),
        name="doctor-appointments-list",
    ),
    # ---------------- Doctor Specialty -------------------------
    path(
        "/specialties/<uuid:doctor_specialty_uuid>",
        views.PrivateDoctorSpecialtyConnectorRetrieveUpdateDestroy.as_view(),
        name="doctor-specialty-connector-detail",
    ),
    path(
        "/specialties",
        views.PrivateDoctorSpecialtyConnectorListCreate.as_view(),
        name="doctor-specialty-connector-list-create",
    ),
    # --------------------- Doctor Registration -----------------------------
    path(
        "/profile",
        views.PrivateDoctorRetrieveUpdateDestroy.as_view(),
        name="doctor-detail",
    ),
    path(
        "/profile/update",
        views.PrivateDoctorProfileUpdate.as_view(),
        name="doctor-create",
    ),
]
