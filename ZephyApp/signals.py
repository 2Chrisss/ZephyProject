from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Box
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Box)
def notificar_cambio_box(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    estado = instance.estadobox_idestadobox.nombre

    # Define la clase CSS según el estado
    status_class = 'bg-success' if estado == 'Disponible' else (
        'bg-danger' if estado == 'Ocupado' else 'bg-warning text-dark'
    )

    # Envía el mensaje al grupo de WebSocket
    async_to_sync(channel_layer.group_send)(
        "boxes_updates",  # Grupo que están escuchando los clientes
        {
            'type': 'box_update',
            'box_id': instance.idbox,
            'box_number': instance.numerobox,
            'new_status_class': status_class,
        }
    )
