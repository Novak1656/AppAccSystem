from django.apps import AppConfig


class StuffAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stuff_app'
    verbose_name = 'Приложение сотрудников'
