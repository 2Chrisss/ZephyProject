# ZephyReportes/routing.py
from django.urls import re_path
from .consumers import BoxConsumer

websocket_urlpatterns = [
    re_path(r'ws/boxes/$', BoxConsumer.as_asgi()),  # Asegúrate de que esta URL coincida
]
