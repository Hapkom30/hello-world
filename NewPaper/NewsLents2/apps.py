from django.apps import AppConfig


class Newslents2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NewsLents2'

    def ready(self):
        from . import signals # выполнение модуля -> регистрация сигналов