from django.urls import path
from . import views

urlpatterns = [
    path(
        "/appointments/<uuid:appointment_uuid>/prescriptions/<uuid:prescription_uuid>",
        views.HospitalDoctorScheduleAppointmentPrescriptionDetail.as_view(),
        name="patient-prescription-detail",
    ),
    path(
        "/appointments/<uuid:appointment_uuid>/prescriptions",
        views.HospitalDoctorScheduleAppointmentPrescription.as_view(),
        name="patient-prescription-list",
    ),
    path(
        "/appointments/<uuid:appointment_uuid>",
        views.HospitalDoctorScheduleAppointmentDetail.as_view(),
        name="patient-prescription-create-list",
    ),
    path(
        "/hospitals/<uuid:hospital_uuid>/appointments/<uuid:appointment_uuid>",
        views.DoctorAppointmentRetrieveUpdateDestroy.as_view(),
        name="patient-doctor-booking-detail",
    ),
    path(
        "/appointments",
        views.PatientDoctorAppointmentListCreate.as_view(),
        name="patient-doctor-appointment-list",
    ),
]
