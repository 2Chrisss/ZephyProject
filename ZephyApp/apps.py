from django.apps import AppConfig

class ZephyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ZephyApp'

    def ready(self):
        import ZephyApp.signals
        from ZephyApp.tasks import start_task  #  importa la función
        start_task()  #  inicia el hilo de revisión de boxes