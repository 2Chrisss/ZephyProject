from django.shortcuts import render, get_object_or_404, redirect
from collections import defaultdict
from .models import *  
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from datetime import time,datetime

def dashboard(request):
    box_disponibles = Box.objects.filter(estadobox_idestadobox='1').count()
    box_ocupados = Box.objects.filter(estadobox_idestadobox='2').count()
    box_no_disponibles = Box.objects.filter(estadobox_idestadobox='3').count()
    return render(request, 'dashboard.html', {
        'box_disponibles': box_disponibles,
        'box_ocupados': box_ocupados,
        'box_no_disponibles': box_no_disponibles,
    })
def calcular_porcentaje_ocupacion(box, fecha=None):
    if fecha:
        fecha_filtro = timezone.datetime.strptime(fecha, "%Y-%m-%d").date()
    else:
        fecha_filtro = timezone.now().date()

    ocupaciones = Boxprofesional.objects.filter(
        box_idbox=box,
        fechaasignacion__lte=fecha_filtro,
        fechatermino__gte=fecha_filtro
    )

    total_am = 0
    total_pm = 0

    for ocupacion in ocupaciones:
        if ocupacion.horarioinicio < time(12, 0):
            fin_am = min(ocupacion.horariofin, time(12, 0))
            total_am += (fin_am.hour * 60 + fin_am.minute) - (ocupacion.horarioinicio.hour * 60 + ocupacion.horarioinicio.minute)
        if ocupacion.horariofin > time(12, 0):
            inicio_pm = max(ocupacion.horarioinicio, time(12, 0))
            total_pm += (ocupacion.horariofin.hour * 60 + ocupacion.horariofin.minute) - (inicio_pm.hour * 60 + inicio_pm.minute)

    porcentaje_am = (total_am / (12 * 60)) * 100
    porcentaje_pm = (total_pm / (5 * 60)) * 100

    return round(porcentaje_am, 2), round(porcentaje_pm, 2)

def box_list(request):
    estado = request.GET.get('estado', '')
    pasillo = request.GET.get('pasillo', '')
    fecha_str = request.GET.get('fecha', '')
    horario = request.GET.get('horario', '')  

    todos_los_pasillos = Pasillobox.objects.values_list('nombre', flat=True).distinct()
    pasillos=  Pasillobox.objects.all().order_by('idpasillobox')
    boxes = Box.objects.exclude(idbox__isnull=True).order_by('numerobox')

    if estado:
        boxes = boxes.filter(estadobox_idestadobox=estado)
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
            box_idbox=box,
            fechaasignacion__lte=fecha,
            fechatermino__gte=fecha
        )
        if horario == 'AM':
            ocupaciones = ocupaciones.filter(horarioinicio__lt=time(12, 0))
        elif horario == 'PM':
            ocupaciones = ocupaciones.filter(horarioinicio__gte=time(12, 0))

        if ocupaciones.exists() or not fecha_str:
            porcentaje_am, porcentaje_pm = calcular_porcentaje_ocupacion(box, fecha_str)
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
    ocupaciones = Boxprofesional.objects.filter(box_idbox=box).order_by('fechaasignacion')

    # Calcular horas totales y agrupar por doctor
    horas_por_doctor = defaultdict(int)
    for ocupacion in ocupaciones:
        inicio = ocupacion.horarioinicio
        fin = ocupacion.horariofin
        horas_tomadas = (fin.hour * 60 + fin.minute) - (inicio.hour * 60 + inicio.minute)
        horas_por_doctor[ocupacion.profesional_idprofesional.nombre] += horas_tomadas  # Cambiado a 'profesional_idprofesional'

    # Convertir minutos a horas y minutos
    horas_por_doctor = {doctor: f"{horas // 60}h {horas % 60}m" for doctor, horas in horas_por_doctor.items()}

    return render(request, 'box_detalle.html', {
        'box': box,
        'ocupaciones': ocupaciones,
        'horas_por_doctor': horas_por_doctor,
    })

