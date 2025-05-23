from django.db import models
from django.utils import timezone
from datetime import time,datetime, date
from .estado import EstadoDisponible, EstadoOcupado, EstadoNoDisponible

from django.db.models import Avg

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)




class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Especialidad(models.Model):
    idespecialidad = models.IntegerField(db_column='idEspecialidad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=120, blank=True, null=True)
    descripcion = models.CharField(max_length=120, blank=True, null=True)
    def getAllEspecialidades():
        return list(Especialidad.objects.values_list('idEspecialidad', flat=True))

    class Meta:
        managed = False
        db_table = 'especialidad'


class Estadobox(models.Model):
    idestadobox = models.IntegerField(db_column='idestadoBox', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=90, blank=True, null=True)
    estado = models.CharField(db_column='nombre',max_length=200, blank=True, null=True)
    def getEstadoBox(idestado: int):
        return EstadoBox.objects.filter(id=idestadobox).values_list('nombre', flat=True).first()

    def getAllEstados():
        return list(EstadoBox.objects.values_list('nombre', flat=True))

    def getAll_idEstado():
        return list(EstadoBox.objects.values_list('idEstadoBox', flat=True))
    class Meta:
        managed = False
        db_table = 'estadobox'


class Pasillobox(models.Model):
    idpasillobox = models.AutoField(db_column='idPasilloBox', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45, blank=True, null=True)
    def getPasilloBox():
        return list(PasilloBox.objects.values_list('nombrebox', flat=True))

    def getAllPasilloBox():
        return list(PasilloBox.objects.values_list('nombrebox', flat=True))
    class Meta:
        managed = False
        db_table = 'pasillobox'


class Profesional(models.Model):
    idprofesional = models.IntegerField(db_column='idProfesional', primary_key=True)  # Field name made lowercase.
    especialidad_idespecialidad = models.ForeignKey(Especialidad, models.DO_NOTHING, db_column='Especialidad_idEspecialidad')  # Field name made lowercase.
    rutprofesional = models.CharField(db_column='rutProfesional', max_length=45, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45, blank=True, null=True)
    apellido = models.CharField(max_length=90, blank=True, null=True)
    email = models.CharField(max_length=320, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    def getAllProfesionales():
        return list(Profesional.objects.values_list('rutProfesional', flat=True))

    def getProfessional(rut: str):
        return Profesional.objects.filter(rutprofesional=rut).first()

    class Meta:
        managed = False
        db_table = 'profesional'

class Box(models.Model):
    idbox = models.AutoField(db_column='idBox', primary_key=True)  # Field name made lowercase.
    estadobox_idestadobox = models.ForeignKey('Estadobox', models.DO_NOTHING, db_column='estadoBox_idestadoBox')  # Field name made lowercase.
    numerobox = models.CharField(db_column='numeroBox', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ubicacionbox = models.CharField(db_column='ubicacionBox', max_length=200, blank=True, null=True)  # Field name made lowercase.
    pasillobox_idpasillobox = models.ForeignKey('Pasillobox', models.DO_NOTHING, db_column='pasilloBox_idPasilloBox', blank=True, null=True)  # Field name made lowercase.
    def get_porcentajes(self):
        box_profesionales = Boxprofesional.objects.filter(idbox=self)
        porcentaje_am = box_profesionales.aggregate(avg_am=Avg('porcentaje_am'))['avg_am'] or 0
        porcentaje_pm = box_profesionales.aggregate(avg_pm=Avg('porcentaje_pm'))['avg_pm'] or 0
        return porcentaje_am, porcentaje_pm
    def get_estado_instance(self):
        if self.estadobox_idestadobox_id == 1:
            return EstadoDisponible(self)
        elif self.estadobox_idestadobox_id == 3:
            return EstadoNoDisponible(self)
        elif self.estadobox_idestadobox_id == 2:
            return EstadoOcupado(self)
        else:
            return None
    class Meta:
        managed = False
        db_table = 'box'


class Boxprofesional(models.Model):
    idboxprofesional = models.AutoField(db_column='idBoxProfesionalcol', primary_key=True)  # Field name made lowercase.
    idbox = models.ForeignKey(Box, models.DO_NOTHING, db_column='Box_idBox')  # Field name made lowercase.
    idprofesional = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='Profesional_idProfesional')  # Field name made lowercase.
    fechaasignacion = models.DateField(db_column='fechaAsignacion', blank=True, null=True)  # Field name made lowercase.
    fechatermino = models.DateField(db_column='fechaTermino', blank=True, null=True)  # Field name made lowercase.
    horarioinicio = models.TimeField(db_column='horarioInicio', blank=True, null=True)  # Field name made lowercase.
    horariofin = models.TimeField(db_column='horarioFin', blank=True, null=True)  # Field name made lowercase.

    
    @staticmethod
    def calcular_porcentaje_ocupacion_con_ocupaciones(ocupaciones):
        horas_am_ocupadas = 0
        minutos_am_ocupados = 0
        horas_pm_ocupadas = 0
        minutos_pm_ocupados = 0

        inicio_am = 8 * 60        
        fin_am = 12 * 60         
        inicio_pm = 12 * 60       
        fin_pm = 17 * 60 + 30     

        for ocupacion in ocupaciones:
            inicio_ocup = ocupacion.horarioinicio.hour * 60 + ocupacion.horarioinicio.minute
            fin_ocup = ocupacion.horariofin.hour * 60 + ocupacion.horariofin.minute

            inicio_am_ocup = max(inicio_ocup, inicio_am)
            fin_am_ocup = min(fin_ocup, fin_am)
            if fin_am_ocup > inicio_am_ocup:
                minutos_am_ocupados += fin_am_ocup - inicio_am_ocup

            inicio_pm_ocup = max(inicio_ocup, inicio_pm)
            fin_pm_ocup = min(fin_ocup, fin_pm)
            if fin_pm_ocup > inicio_pm_ocup:
                minutos_pm_ocupados += fin_pm_ocup - inicio_pm_ocup

        porcentaje_am = (minutos_am_ocupados / ((fin_am - inicio_am))) * 100
        porcentaje_pm = (minutos_pm_ocupados / ((fin_pm - inicio_pm))) * 100

        return round(porcentaje_am, 2), round(porcentaje_pm, 2)

    class Meta:
        managed = False
        db_table = 'boxprofesional'
