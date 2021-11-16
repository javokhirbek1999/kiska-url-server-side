from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self) -> None:
        from .signals.create_urls_signal import create_original_url
        from .signals.create_short_url_signal import create_short_url
        from .signals.create_all_short_url_signal import create_all_short_url