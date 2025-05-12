from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .dashboard import obtener_estadisticas

def send_dashboard_update():
    channel_layer = get_channel_layer()
    data = obtener_estadisticas()
    async_to_sync(channel_layer.group_send)(
        "dashboard",
        {
            "type": "dashboard.update",
            "data": data,
        },
    )