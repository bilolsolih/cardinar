from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AboutConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _('Footer')
    name = "apps.about"

    def ready(self):
        import apps.about.signals  # noqa
