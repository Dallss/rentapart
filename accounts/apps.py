from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import accounts.signals

        if not settings.GOOGLE_CLIENT_ID:
            raise ImproperlyConfigured(
                "GOOGLE_CLIENT_ID is required"
            )