from django.shortcuts import render, get_object_or_404, redirect
from collections import defaultdict
from .models import *  # Asegúrate de que el modelo Box esté importado

def box_list(request):
    boxes = Box.objects.all().order_by('numerobox')
    boxes_por_pasillo = defaultdict(list)

    for box in boxes:
        pasillo = box.ubicacionbox  # "Pasillo 1", "Pasillo 2", etc.
        boxes_por_pasillo[pasillo].append(box)

    return render(request, 'box_list.html', {
        'boxes_por_pasillo': dict(boxes_por_pasillo)
    })
def cambiar_estado_box(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    estados = Estadobox.objects.all()

    if request.method == 'POST':
        nuevo_estado_id = request.POST.get('estado')
        nuevo_estado = get_object_or_404(Estadobox, pk=nuevo_estado_id)
        box.estadobox_idestadobox = nuevo_estado
        box.save()
        return redirect('box_list')  # o a donde quieras redirigir

    return render(request, 'cambiar_estado.html', {
        'box': box,
        'estados': estados
    })
