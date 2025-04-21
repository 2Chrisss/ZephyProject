from django.db import models


class Especialidad(models.Model):
    idespecialidad = models.IntegerField(db_column='idEspecialidad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=120, blank=True, null=True)
    descripcion = models.CharField(max_length=120, blank=True, null=True)

    class Meta:

        db_table = 'especialidad'


class Estadobox(models.Model):
    idestadobox = models.IntegerField(db_column='idestadoBox', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=90, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:

        db_table = 'estadobox'


class Profesional(models.Model):
    idprofesional = models.IntegerField(db_column='idProfesional', primary_key=True)  # Field name made lowercase.
    especialidad_idespecialidad = models.ForeignKey(Especialidad, models.DO_NOTHING, db_column='Especialidad_idEspecialidad')  # Field name made lowercase.
    rutprofesional = models.CharField(db_column='rutProfesional', max_length=45, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45, blank=True, null=True)
    apellido = models.CharField(max_length=90, blank=True, null=True)
    email = models.CharField(max_length=320, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
   
        db_table = 'profesional'


class Tipobox(models.Model):
    idtipobox = models.IntegerField(db_column='idtipoBox', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:

        db_table = 'tipobox'
 

class Boxprofesional(models.Model):
    idboxprofesionalcol = models.CharField(db_column='idBoxProfesionalcol', primary_key=True, max_length=45)  # Field name made lowercase.
    box_idbox = models.ForeignKey('Box', models.DO_NOTHING, db_column='Box_idBox')  # Field name made lowercase.
    profesional_idprofesional = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='Profesional_idProfesional')  # Field name made lowercase.
    fechaasignacion = models.DateField(db_column='fechaAsignacion', blank=True, null=True)  # Field name made lowercase.
    fechatermino = models.DateField(db_column='fechaTermino', blank=True, null=True)  # Field name made lowercase.
    horarioinicio = models.TimeField(db_column='horarioInicio', blank=True, null=True)  # Field name made lowercase.
    horariofin = models.TimeField(db_column='horarioFin', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'boxprofesional'
class Box(models.Model):
    idbox = models.IntegerField(db_column='idBox', primary_key=True)  # Field name made lowercase.
    tipobox_idtipobox = models.ForeignKey('Tipobox', models.DO_NOTHING, db_column='tipoBox_idtipoBox')  # Field name made lowercase.
    estadobox_idestadobox = models.ForeignKey('Estadobox', models.DO_NOTHING, db_column='estadoBox_idestadoBox')  # Field name made lowercase.
    numerobox = models.IntegerField(db_column='numeroBox', blank=True, null=True)  # Field name made lowercase.
    ubicacionbox = models.CharField(db_column='ubicacionBox', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'box'


