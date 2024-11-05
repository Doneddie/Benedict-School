from django.apps import AppConfig

class BenedictSchoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'benedict_school'

    def ready(self):
        # Import the signals module so that signals are registered
        import benedict_school.signals
