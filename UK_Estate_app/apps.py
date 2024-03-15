from django.apps import AppConfig


class UkEstateAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "UK_Estate_app"


# your_app/apps.py

from django.apps import AppConfig
from django.db.models.signals import post_migrate

class YourAppConfig(AppConfig):
    name = 'your_app'

    def ready(self):
        from .signals import create_default_group
        post_migrate.connect(create_default_group, sender=self)
