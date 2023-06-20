from django.apps import AppConfig
from django.conf import settings

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        super().ready()
        from tasks import listen_mqtt_topic
        if settings.RUN_RABBITMQ_LISTENER:
            listen_mqtt_topic.delay()
