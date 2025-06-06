from django.apps import AppConfig


class UrfeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'urfe'

    def ready(self):
        import urfe.signals
