import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from ZephyReportes.routing import websocket_urlpatterns as reportes_urlpatterns
from ZephyEstadisticas.routing import websocket_urlpatterns as estadisticas_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZephySite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            reportes_urlpatterns + estadisticas_urlpatterns
        )
    ),
})
