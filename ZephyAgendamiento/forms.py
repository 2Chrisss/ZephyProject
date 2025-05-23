from django import forms
from datetime import time, datetime, timedelta
from ZephyReportes.models import Box, Profesional

def generar_bloques_horarios(hora_inicio=time(8, 0), hora_fin=time(21,0), intervalo=30, excluir_ranges=None):
    excluir_ranges = excluir_ranges or []
    bloques = []
    actual = datetime.combine(datetime.today(), hora_inicio)
    fin = datetime.combine(datetime.today(), hora_fin)

    while actual < fin:
        bloque_inicio = actual.time()
        bloque_str = bloque_inicio.strftime("%H:%M")
        
        ocupado = any(
            bloque_inicio >= datetime.strptime(inicio, "%H:%M").time() and
            bloque_inicio < datetime.strptime(fin, "%H:%M").time()
            for inicio, fin in excluir_ranges
        )

        if not ocupado:
            bloques.append((bloque_str, bloque_str))
        
        actual += timedelta(minutes=intervalo)

    return bloques

class AgendarBoxForm(forms.Form):
    box = forms.ModelChoiceField(
        queryset=Box.objects.all(),
        label="Box",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.all(),
        label="Profesional",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_asignacion = forms.DateField(
        label="Fecha asignación",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )
    fecha_termino = forms.DateField(
        label="Fecha término",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    horario_inicio = forms.ChoiceField(
        label="Horario inicio",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    horario_fin = forms.ChoiceField(
        label="Horario fin",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, horarios_disponibles=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horario_inicio'].choices = horarios_disponibles or generar_bloques_horarios()
        self.fields['horario_fin'].choices = horarios_disponibles or generar_bloques_horarios()
        self.fields['profesional'].queryset = Profesional.objects.all().order_by('nombre')
        self.fields['profesional'].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellido}"
    def clean(self):
        cleaned_data = super().clean()
        horario_inicio = cleaned_data.get('horario_inicio')
        horario_fin = cleaned_data.get('horario_fin')

        if horario_inicio and horario_fin:
            inicio = datetime.strptime(horario_inicio, "%H:%M").time()
            fin = datetime.strptime(horario_fin, "%H:%M").time()
            
            if fin <= inicio:
                self.add_error('horario_fin', 'El horario de fin debe ser posterior al horario de inicio')
            
            delta = datetime.combine(datetime.today(), fin) - datetime.combine(datetime.today(), inicio)
            if delta.total_seconds() < 1800: 
                self.add_error(None, 'La duración mínima del agendamiento debe ser de 30 minutos')

        return cleaned_data