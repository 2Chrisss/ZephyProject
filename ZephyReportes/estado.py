from django.utils import timezone
from datetime import time

class Estado:
    def __init__(self, box):
        self.box = box

    def clickAsignar(self):
        raise NotImplementedError("Método clickAsignar no implementado")

    def clickLiberar(self):
        raise NotImplementedError("Método clickLiberar no implementado")

    def clickNoDisponible(self):
        raise NotImplementedError("Método clickNoDisponible no implementado")

    def puede_agendar(self, fecha, horario_inicio, horario_fin):
        """Verifica si se puede agendar en el estado actual"""
        raise NotImplementedError("Método puede_agendar no implementado")

    def obtener_horarios_disponibles(self, fecha):
        """Obtiene horarios disponibles según el estado"""
        raise NotImplementedError("Método obtener_horarios_disponibles no implementado")


class EstadoDisponible(Estado):
    def clickAsignar(self):
        self.box.estadobox_idestadobox_id = 2  
        self.box.save()

    def clickNoDisponible(self):
        self.box.estadobox_idestadobox_id = 3  
        self.box.save()

    def puede_agendar(self, fecha, horario_inicio, horario_fin):
        from .models import Boxprofesional  
        return not Boxprofesional.objects.filter(
            idbox=self.box,
            fechaasignacion=fecha,
            horarioinicio__lt=horario_fin,
            horariofin__gt=horario_inicio
        ).exists()

    def obtener_horarios_disponibles(self, fecha):
        from ZephyAgendamiento.forms import generar_bloques_horarios
        
        from .models import Boxprofesional  
        ocupados = Boxprofesional.objects.filter(
            idbox=self.box,
            fechaasignacion=fecha
        ).values_list('horarioinicio', 'horariofin')
        
        rangos_ocupados = [
            (inicio.strftime("%H:%M"), fin.strftime("%H:%M")) 
            for inicio, fin in ocupados
        ]
        
        return generar_bloques_horarios(excluir_ranges=rangos_ocupados)


class EstadoOcupado(Estado):
    def clickLiberar(self):
        self.box.estadobox_idestadobox_id = 1  
        self.box.save()

    def clickNoDisponible(self):
        self.box.estadobox_idestadobox_id = 3  
        self.box.save()

    def puede_agendar(self, fecha, horario_inicio, horario_fin):
        from .models import Boxprofesional  
        return not Boxprofesional.objects.filter(
            idbox=self.box,
            fechaasignacion=fecha,
            horarioinicio__lt=horario_fin,
            horariofin__gt=horario_inicio
        ).exists()

    def obtener_horarios_disponibles(self, fecha):
        from ZephyAgendamiento.forms import generar_bloques_horarios
        from .models import Boxprofesional  
        
        ocupados = Boxprofesional.objects.filter(
            idbox=self.box,
            fechaasignacion=fecha
        ).values_list('horarioinicio', 'horariofin')
        
        rangos_ocupados = [
            (inicio.strftime("%H:%M"), fin.strftime("%H:%M")) 
            for inicio, fin in ocupados
        ]
        
        return generar_bloques_horarios(excluir_ranges=rangos_ocupados)


class EstadoNoDisponible(Estado):
    def clickAsignar(self):
        self.box.estadobox_idestadobox_id = 2  
        self.box.save()

    def puede_agendar(self, fecha, horario_inicio, horario_fin):
        return False  

    def obtener_horarios_disponibles(self, fecha):
        return []  