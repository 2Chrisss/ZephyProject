from django.shortcuts import render, get_object_or_404, redirect
from .models import *  # Asegúrate de que el modelo Box esté importado

def box_list(request):
    boxes = Box.objects.all()  
    return render(request, 'box_list.html', {'boxes': boxes})
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