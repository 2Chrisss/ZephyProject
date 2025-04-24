from django.shortcuts import render, get_object_or_404, redirect
from collections import defaultdict
from .models import *  
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

def dashboard(request):
    box_disponibles = Box.objects.filter(estadobox_idestadobox='1').count()
    box_ocupados = Box.objects.filter(estadobox_idestadobox='2').count()
    box_no_disponibles = Box.objects.filter(estadobox_idestadobox='3').count()
    return render(request, 'dashboard.html', {
        'box_disponibles': box_disponibles,
        'box_ocupados': box_ocupados,
        'box_no_disponibles': box_no_disponibles,
    })
def box_list(request):
    
    
    boxes = Box.objects.all().order_by('numerobox')
    boxes_por_pasillo = defaultdict(list)

    for box in boxes:
        pasillo = box.ubicacionbox  
        boxes_por_pasillo[pasillo].append(box)
    return render(request, 'box_list.html', {
        'boxes_por_pasillo': dict(boxes_por_pasillo)

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