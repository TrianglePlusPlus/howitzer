from django.apps import AppConfig

class MainAppConfig(AppConfig):
    name = 'app'
    verbose_name = "Square Connect Main App"

    def ready(self):
        from app.models import Service
        try:
            if Service.objects.count() == 0:
                Service.regenerate_services()
        except:
            # This is necessary for when making preliminary migrations
            # If you change this format Django will attempt to use
            # a table before it exists.
            pass
