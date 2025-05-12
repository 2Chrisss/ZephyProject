# zephy/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from ZephyReportes.routing import websocket_urlpatterns as reportes_ws
from ZephyEstadisticas.routing import websocket_urlpatterns as estadisticas_ws

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            reportes_ws + estadisticas_ws
        )
    ),
})
