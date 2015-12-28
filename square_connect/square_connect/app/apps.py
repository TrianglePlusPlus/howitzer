from django.apps import AppConfig

class MainAppConfig(AppConfig):
    name = 'app'
    verbose_name = "Square Connect Main App"

    def ready(self):
        from app.models import Service
        if Service.objects.count() == 0:
            Service.regenerate_services()
