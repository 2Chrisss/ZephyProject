from django.shortcuts import render, get_object_or_404, redirect
from collections import defaultdict
from .models import *  
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from datetime import time,datetime, date

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
    estado = request.GET.get('estado', '')
    pasillo = request.GET.get('pasillo', '')
    fecha_str = request.GET.get('fecha', '')
    horario = request.GET.get('horario', '')

    todos_los_pasillos = Pasillobox.objects.values_list('nombre', flat=True).distinct()
    boxes = Box.objects.all().order_by('numerobox')

    if estado:
        try:
            estado_id = int(estado)
            boxes = boxes.filter(estadobox_idestadobox=estado_id)
        except ValueError:
            pass

    if pasillo:
        boxes = boxes.filter(pasillobox_idpasillobox__nombre=pasillo)

    if fecha_str:
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            fecha = timezone.now().date()
    else:
        fecha = timezone.now().date()

    boxes_por_pasillo = defaultdict(list)

    for box in boxes:
        ocupaciones = Boxprofesional.objects.filter(
            idbox=box,
            fechaasignacion__lte=fecha,
            fechatermino__gte=fecha
        )

        if horario == 'AM':
            ocupaciones = ocupaciones.filter(horarioinicio__lt=time(12, 0))
        elif horario == 'PM':
            ocupaciones = ocupaciones.filter(horarioinicio__gte=time(12, 0))

        if ocupaciones.exists() or not fecha_str:
            porcentaje_am, porcentaje_pm = Boxprofesional.calcular_porcentaje_ocupacion_con_ocupaciones(ocupaciones)
            pasillo_nombre = box.pasillobox_idpasillobox.nombre
            boxes_por_pasillo[pasillo_nombre].append({
                'box': box,
                'porcentaje_am': porcentaje_am,
                'porcentaje_pm': porcentaje_pm
            })

    return render(request, 'box_list.html', {
        'boxes_por_pasillo': dict(boxes_por_pasillo),
        'todos_los_pasillos': todos_los_pasillos,
        'fecha_filtro': fecha_str,
        'horario_filtro': horario,
    })


def box_detalle(request, box_id):
    box = get_object_or_404(Box, idbox=box_id)
    ocupaciones_qs = Boxprofesional.objects.filter(
        idbox=box,
        fechaasignacion=date.today()
    ).order_by('fechaasignacion')

    ocupaciones = []
    horas_por_doctor = defaultdict(int)
    for ocupacion in ocupaciones_qs:
        inicio_min = ocupacion.horarioinicio.hour * 60 + ocupacion.horarioinicio.minute
        fin_min = ocupacion.horariofin.hour * 60 + ocupacion.horariofin.minute
        duracion = fin_min - inicio_min
        horas_por_doctor[ocupacion.idprofesional.nombre] += duracion
        ocupaciones.append({
            'profesional': ocupacion.idprofesional,
            'inicio_min': inicio_min,
            'fin_min': fin_min,
        })

    horas_por_doctor_fmt = {doctor: f"{minutos // 60}h {minutos % 60}m" for doctor, minutos in horas_por_doctor.items()}

    intervalos = []
    start = 8 * 60
    end = 17 * 60 + 30
    for minutos in range(start, end + 1, 30):
        h = minutos // 60
        m = minutos % 60
        intervalos.append({'label': f"{h:02d}:{m:02d}", 'total_min': minutos})

    return render(request, 'box_detalle.html', {
        'box': box,
        'ocupaciones': ocupaciones,
        'horas_por_doctor': horas_por_doctor_fmt,
        'intervalos': intervalos,
    })

