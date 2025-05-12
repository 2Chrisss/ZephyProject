from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from ZephyReportes.models import Box, Boxprofesional
from datetime import time
from .dashboard import obtener_estadisticas
from django.db.models import Q

def dashboard(request):

    estadisticas = obtener_estadisticas()
    return render(request, 'dashboard.html', {'estadisticas': estadisticas})

