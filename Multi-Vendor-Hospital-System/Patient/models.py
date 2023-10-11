from django.db import models
from datetime import date

# Create your models here.


from Accounts.models import User
from Doctor.models import DoctorScheduleDaysConnector, EmergencyDoctorScedule
from Common.models import BaseModelWithUID, Medical_Test, Medicine

# from Hospital.models import Hospital


class DoctorAppointment(BaseModelWithUID):
    doctor_schedule_day = models.ForeignKey(
        DoctorScheduleDaysConnector, on_delete=models.CASCADE
    )
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    isnotified = models.BooleanField(default=False)
    serial_no = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return self.patient.first_name + " " + str(self.date)

    # def __str__(self):
    #     return f"Doctor: {self.doctor_schedule_day.doctor_schedule.doctor.doctor_info.first_name} - Patient: {self.patient.first_name} - Date: {self.date}"


class EmergencyDoctorAppointment(BaseModelWithUID):
    doctor_schedule_date = models.ForeignKey(
        EmergencyDoctorScedule, on_delete=models.CASCADE
    )
    patient = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Doctor: {self.doctor_schedule_day.doctor_schedule.doctor.doctor_info.first_name} - Patient: {self.patient.first_name} - Date: {self.doctor_schedule_date.schedule_date}"


class Prescription(BaseModelWithUID):
    patient_doctor_booking = models.ForeignKey(
        DoctorAppointment, on_delete=models.CASCADE
    )
    prescription_date = models.DateField(default=date.today)
    previous_medications = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient_doctor_booking}"


class PrescriptionMedicalTestConnector(BaseModelWithUID):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    test = models.ForeignKey(Medical_Test, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Prescription:{self.prescription} Test:{self.test}"


class PrescriptionMedicineConnector(BaseModelWithUID):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.prescription} {self.medicine}"
