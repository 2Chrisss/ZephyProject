from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/boxes/', consumers.BoxConsumer.as_asgi()),  
]