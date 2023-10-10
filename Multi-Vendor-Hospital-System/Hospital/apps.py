from django.apps import AppConfig


class HospitalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Hospital"

    def ready(self) -> None:
        import Hospital.signals
