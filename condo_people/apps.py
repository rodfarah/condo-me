from django.apps import AppConfig


class CondoPeopleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "condo_people"
    verbose_name = "Condo Users"

    def ready(self) -> None:
        from . import signals  # noqa: F401
