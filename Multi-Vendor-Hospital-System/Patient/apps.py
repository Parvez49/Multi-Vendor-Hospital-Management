from django.apps import AppConfig


class PatientConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Patient"

    def ready(self) -> None:
        import Patient.signals

        # return super().ready()
