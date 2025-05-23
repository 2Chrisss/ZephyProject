from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Box
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ZephyEstadisticas.signals import send_dashboard_update

@receiver(post_save, sender=Box)
def notificar_cambio_box(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    estado = instance.estadobox_idestadobox.nombre

    status_class = 'bg-disponible' if estado == 'Disponible' else (
        'bg-ocupado' if estado == 'Ocupado' else 'bg-no-disponible'
    )

    # Obtener asignaciones activas
    tz = pytz.timezone('America/Santiago')
    now = datetime.now(tz)
    current_date = now.date()
    current_time = now.time()

    asignaciones_activas = Boxprofesional.objects.filter(
        fechaasignacion__lte=current_date,
        fechatermino__gte=current_date,
        horarioinicio__lte=current_time,
        horariofin__gte=current_time
    )

    porcentaje_am, porcentaje_pm = Boxprofesional.calcular_porcentaje_ocupacion_con_ocupaciones(asignaciones_activas)

    async_to_sync(channel_layer.group_send)(
        "boxes_updates",
        {
            'type': 'box_update',
            'box_id': instance.idbox,
            'box_number': instance.numerobox,
            'new_status_class': status_class,
            'porcentaje_am': porcentaje_am,
            'porcentaje_pm': porcentaje_pm,
        }
    )
@receiver(post_save, sender=Box)
def actualizar_dashboard_post_save(sender, instance, created, **kwargs):
    send_dashboard_update()