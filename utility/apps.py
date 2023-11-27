from django.apps import AppConfig


class UtilityConfig(AppConfig):
    name = 'utility'

    def ready(self):
        import utility.signals
