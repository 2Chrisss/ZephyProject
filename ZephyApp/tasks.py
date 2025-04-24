import threading
import time
from django.utils import timezone
from .models import Boxprofesional, Estadobox
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
import pytz  # Para manejar la zona horaria explícitamente

def check_and_update_boxes():
    while True:
        tz = pytz.timezone('America/Santiago')
        now = datetime.now(tz).replace(microsecond=0)
        current_date = now.date()
        current_time = now.time()

        try:
            ocupado_estado = Estadobox.objects.get(nombre="Ocupado")
            disponible_estado = Estadobox.objects.get(nombre="Disponible")

            # 1. MARCAR COMO OCUPADOS si está dentro del horario de alguna asignación
            asignaciones_activas = Boxprofesional.objects.select_related(
                'box_idbox', 'box_idbox__estadobox_idestadobox'
            ).filter(
                fechaasignacion__lte=current_date,
                fechatermino__gte=current_date,
                horarioinicio__lte=current_time,
                horariofin__gte=current_time
            )

            boxes_ocupados_ids = set()

            for asignacion in asignaciones_activas:
                box = asignacion.box_idbox
                boxes_ocupados_ids.add(box.idbox)

                if box.estadobox_idestadobox != ocupado_estado:
                    box.estadobox_idestadobox = ocupado_estado
                    box.save()

                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "boxes_updates",
                        {
                            'type': 'box_update',
                            'box_id': box.idbox,
                            'box_number': box.numerobox,
                            'new_status_class': 'bg-danger'

                        }
                    )

            # 2. MARCAR COMO DISPONIBLES todos los boxes que NO están en boxes_ocupados_ids
            boxes_disponibles = Boxprofesional.objects.select_related(
                'box_idbox', 'box_idbox__estadobox_idestadobox'
            ).filter(
                fechatermino__lt=current_date
            ) | Boxprofesional.objects.select_related(
                'box_idbox', 'box_idbox__estadobox_idestadobox'
            ).filter(
                fechatermino=current_date,
                horariofin__lt=current_time
            )

            for asignacion in boxes_disponibles:
                box = asignacion.box_idbox

                # Si este box no fue marcado como ocupado este ciclo
                if box.idbox not in boxes_ocupados_ids and box.estadobox_idestadobox != disponible_estado:
                    box.estadobox_idestadobox = disponible_estado
                    box.save()

                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "boxes_updates",
                        {
                            'type': 'box_update',
                            'box_id': box.idbox,
                            'box_number': box.numerobox,
                            'new_status_class': 'bg-success'
                        }
                    )

        except Exception as e:
            print(f"[ERROR] {str(e)}")

        time.sleep(5)


def start_task():
    thread = threading.Thread(target=check_and_update_boxes, daemon=True)
    thread.start()
