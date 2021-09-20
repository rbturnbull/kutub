from django.apps import AppConfig

class KutubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kutub'

    def ready(self):
        try:
            from watson import search as watson
            watson.register(self.get_model("Manuscript"))
            watson.register(self.get_model("Repository"))
            watson.register(self.get_model("ContentItem"))
        except ImportError:
            import logging
            logging.error("Could not register models for searching with django-watson.")

