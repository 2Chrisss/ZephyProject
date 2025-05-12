# ZephyReportes/apps.py
from django.apps import AppConfig

class ZephyReportesAppConfig(AppConfig):
    name = 'ZephyReportes'

    def ready(self):
        from .tasks import start_task
        start_task()
