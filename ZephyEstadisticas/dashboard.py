from asgiref.sync import sync_to_async
@sync_to_async
def obtener_estadisticas():
    from ZephyReportes.models import Box, Boxprofesional
    from datetime import time, datetime, timedelta
    from django.db.models import Count
    box_disponibles = Box.objects.filter(estadobox_idestadobox=1).count()
    box_ocupados = Box.objects.filter(estadobox_idestadobox=2).count()
    box_no_disponibles = Box.objects.filter(estadobox_idestadobox=3).count()
    

    intervalos = [
        time(8, 0), time(8, 30), time(9, 0), time(9, 30), time(10, 0), time(10, 30),
        time(11, 0), time(11, 30), time(12, 0), time(12, 30), time(13, 0), time(13, 30),
        time(14, 0), time(14, 30), time(15, 0), time(15, 30), time(16, 0), time(16, 30),
        time(17, 0), time(17, 30)
    ]
    ocupacion_por_intervalo = []
    for intervalo in intervalos:
        ocupados = Boxprofesional.objects.filter(
            horarioinicio__lte=intervalo,
            horariofin__gte=intervalo
        ).count()
        disponibles = Box.objects.count() - ocupados
        
        ocupacion_por_intervalo.append({
            'intervalo': intervalo.strftime('%H:%M'),
            'ocupados': ocupados,
            'disponibles': disponibles
        })
    hoy = datetime.now().date()

    boxes_poco_ocupados = Boxprofesional.objects.filter(
        fechaasignacion=hoy,
    ).values(
        'box_idbox__numerobox'
    ).annotate(
        total_ocupaciones=Count('idboxprofesionalcol')
    ).order_by('total_ocupaciones')[:5]

    if len(boxes_poco_ocupados) < 5:
        boxes_sin_ocupaciones = Box.objects.exclude(
            idbox__in=Boxprofesional.objects.filter(
                fechaasignacion=hoy
            ).values_list('box_idbox', flat=True)
        ).values('numerobox')[:5 - len(boxes_poco_ocupados)]
        
        for box in boxes_sin_ocupaciones:
            boxes_poco_ocupados.append({
                'box_idbox__numerobox': box['numerobox'],
                'total_ocupaciones': 0
            })

    top_poco_ocupados = {
        'labels': [box['box_idbox__numerobox'] for box in boxes_poco_ocupados],
        'data': [box['total_ocupaciones'] for box in boxes_poco_ocupados]
    }

    return {
        "box_disponibles": box_disponibles,
        "box_ocupados": box_ocupados,
        "box_no_disponibles": box_no_disponibles,
        "ocupacion_por_intervalo": ocupacion_por_intervalo,
        "top_poco_ocupados": top_poco_ocupados
    }
    return {
        "box_disponibles": box_disponibles,
        "box_ocupados": box_ocupados,
        "box_no_disponibles": box_no_disponibles,
        "ocupacion_por_intervalo": ocupacion_por_intervalo,
        "top_poco_ocupados": top_poco_ocupados
    }