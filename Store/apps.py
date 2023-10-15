from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Store'

    def ready(self) -> None:
        import Store.signals.handlers
