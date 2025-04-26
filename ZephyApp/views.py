from django.shortcuts import render, get_object_or_404, redirect
from collections import defaultdict
from .models import *  
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from datetime import time

def dashboard(request):
    box_disponibles = Box.objects.filter(estadobox_idestadobox='1').count()
    box_ocupados = Box.objects.filter(estadobox_idestadobox='2').count()
    box_no_disponibles = Box.objects.filter(estadobox_idestadobox='3').count()
    return render(request, 'dashboard.html', {
        'box_disponibles': box_disponibles,
        'box_ocupados': box_ocupados,
        'box_no_disponibles': box_no_disponibles,
    })
def calcular_porcentaje_ocupacion(box):
    ocupaciones = Boxprofesional.objects.filter(
        box_idbox=box,
        fechaasignacion__lte=timezone.now().date(),
        fechatermino__gte=timezone.now().date()
    )
    total_am = 0
    total_pm = 0

    for ocupacion in ocupaciones:
        if ocupacion.horarioinicio < time(12, 0):  # AM
            fin_am = min(ocupacion.horariofin, time(12, 0))
            total_am += (fin_am.hour * 60 + fin_am.minute) - (ocupacion.horarioinicio.hour * 60 + ocupacion.horarioinicio.minute)
        if ocupacion.horariofin > time(12, 0):  # PM
            inicio_pm = max(ocupacion.horarioinicio, time(12, 0))
            total_pm += (ocupacion.horariofin.hour * 60 + ocupacion.horariofin.minute) - (inicio_pm.hour * 60 + inicio_pm.minute)

    porcentaje_am = (total_am / (12 * 60)) * 100  # 12 horas en minutos
    porcentaje_pm = (total_pm / (5 * 60)) * 100

    return round(porcentaje_am, 2), round(porcentaje_pm, 2)

def box_list(request):
    estado = request.GET.get('estado', '')
    pasillo = request.GET.get('pasillo', '')

    # Obtener todos los pasillos únicos antes del filtro
    todos_los_pasillos = Box.objects.exclude(idbox__isnull=True).values_list('ubicacionbox', flat=True).distinct()

    # Aplicar filtros
    boxes = Box.objects.exclude(idbox__isnull=True).order_by('numerobox')
    if estado:
        boxes = boxes.filter(estadobox_idestadobox=estado)
    if pasillo:
        boxes = boxes.filter(ubicacionbox=pasillo)

    boxes_por_pasillo = defaultdict(list)
    for box in boxes:
        pasillo_box = box.ubicacionbox
        porcentaje_am, porcentaje_pm = calcular_porcentaje_ocupacion(box)
        boxes_por_pasillo[pasillo_box].append({
            'box': box,
            'porcentaje_am': porcentaje_am,
            'porcentaje_pm': porcentaje_pm
        })

    return render(request, 'box_list.html', {
        'boxes_por_pasillo': dict(boxes_por_pasillo),
        'todos_los_pasillos': todos_los_pasillos,
    })
    
def get_css_class_for_status(status_name):
    if status_name == 'Disponible':
        return 'bg-success'
    elif status_name == 'Ocupado':
        return 'bg-danger'
    elif status_name == 'No disponible':
        return 'bg-warning text-dark'
    else:
        return 'bg-secondary'

def cambiar_estado_box(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    estados = Estadobox.objects.all()

    if request.method == 'POST':
        nuevo_estado_id = request.POST.get('estado')
        nuevo_estado = get_object_or_404(Estadobox, pk=nuevo_estado_id)
        box.estadobox_idestadobox = nuevo_estado
        box.save()

        channel_layer = get_channel_layer()


        status_classes = {
            'Disponible': 'bg-success',
            'Ocupado': 'bg-danger',
            'No disponible': 'bg-warning text-dark'
        }

        new_status_class = status_classes.get(nuevo_estado.nombre, 'bg-secondary')

        async_to_sync(channel_layer.group_send)(
            "boxes_updates",
            {
                'type': 'box_update',
                'box_id': box.idbox,
                'box_number': box.numerobox,
                'new_status_class': new_status_class
            }
        )


        return redirect('box_list')

    return render(request, 'cambiar_estado.html', {
        'box': box,
        'estados': estados
    })

def get_css_class_for_status(status_name):
    if status_name == 'Disponible':
        return 'bg-success'
    elif status_name == 'Ocupado':
        return 'bg-danger'
    elif status_name == 'No disponible':
        return 'bg-warning text-dark'
    else:
        return 'bg-secondary'

