from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, time, date
from .forms import AgendarBoxForm, generar_bloques_horarios
from ZephyReportes.models import Boxprofesional, Box, Profesional
from ZephyReportes.estado import EstadoDisponible, EstadoOcupado, EstadoNoDisponible
from django.utils.timezone import now
def obtener_rangos_ocupados(box, fecha):
    """Obtiene los rangos horarios ocupados usando el patrón State"""
    estado = box.get_estado_instance()
    if isinstance(estado, EstadoOcupado):
        agendamientos = Boxprofesional.objects.filter(
            idbox=box,
            fechaasignacion=fecha
        ).order_by('horarioinicio')
        return [(ag.horarioinicio.strftime("%H:%M"), ag.horariofin.strftime("%H:%M")) 
                for ag in agendamientos]
    return []

def agendar_box(request):
    today = now().date()
    boxes = Box.objects.all().order_by('numerobox')
    box_seleccionado = request.GET.get('box')
    fecha_seleccionada = request.GET.get('fecha_asignacion')
    box_obj = None
    rangos_ocupados = []
    horarios_disponibles = []
    
    if box_seleccionado and fecha_seleccionada:
        try:
            box_obj = Box.objects.get(pk=box_seleccionado)
            estado = box_obj.get_estado_instance()
            
            horarios_disponibles = estado.obtener_horarios_disponibles(fecha_seleccionada)
            
            rangos_ocupados = obtener_rangos_ocupados(box_obj, fecha_seleccionada)
            
        except Box.DoesNotExist:
            messages.error(request, "Box no encontrado")
            box_seleccionado = None
    
    if request.method == 'POST':
        form = AgendarBoxForm(request.POST, horarios_disponibles=horarios_disponibles)
        
        if form.is_valid():
            try:
                box = form.cleaned_data['box']
                estado = box.get_estado_instance()
                
                if not estado.puede_agendar(
                    form.cleaned_data['fecha_asignacion'],
                    datetime.strptime(form.cleaned_data['horario_inicio'], "%H:%M").time(),
                    datetime.strptime(form.cleaned_data['horario_fin'], "%H:%M").time()
                ):
                    raise ValueError("No se puede agendar en el estado actual del box")
                
                # Crear el agendamiento
                Boxprofesional.objects.create(
                    idbox=box,
                    idprofesional=form.cleaned_data['profesional'],
                    fechaasignacion=form.cleaned_data['fecha_asignacion'],
                    fechatermino=form.cleaned_data['fecha_termino'],
                    horarioinicio=datetime.strptime(form.cleaned_data['horario_inicio'], "%H:%M").time(),
                    horariofin=datetime.strptime(form.cleaned_data['horario_fin'], "%H:%M").time()
                )
                
                fecha_actual = now().date()
                hora_actual = now().time()
                horario_inicio = datetime.strptime(form.cleaned_data['horario_inicio'], "%H:%M").time()
                horario_fin = datetime.strptime(form.cleaned_data['horario_fin'], "%H:%M").time()

                if (form.cleaned_data['fecha_asignacion'] == fecha_actual and 
                    horario_inicio <= hora_actual <= horario_fin):
                    if isinstance(estado, EstadoDisponible):
                        estado.clickAsignar()
                # Enviar actualización a través del WebSocket
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "boxes_updates",  # Este debe coincidir con el group_name en tu consumer
                    {
                        'type': 'box_update',
                        'box_id': box.idbox,
                        'box_number': box.numerobox,
                        'new_status_class': 'bg-ocupado',  # Clase CSS para estado ocupado
                    }
                )
                
                messages.success(request, "Agendamiento creado exitosamente")
                return redirect('agendar_box')
                
            except Exception as e:
                messages.error(request, f"Error al agendar: {str(e)}")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario")
    else:
        form = AgendarBoxForm(horarios_disponibles=horarios_disponibles)
    
    if box_seleccionado:
        form.fields['box'].initial = box_seleccionado
    if fecha_seleccionada:
        form.fields['fecha_asignacion'].initial = fecha_seleccionada
    
    return render(request, 'agendar_box.html', {
        'form': form,
        'boxes': boxes,
        'box_seleccionado': box_seleccionado,
        'box': box_obj,  
        'fecha_seleccionada': fecha_seleccionada,
        'rangos_ocupados': rangos_ocupados,
        'horarios_disponibles': horarios_disponibles,
        'today': today,
    })