# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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

    class Meta:
        managed = False
        db_table = 'especialidad'


class Estadobox(models.Model):
    idestadobox = models.IntegerField(db_column='idestadoBox', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=90, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estadobox'


class Pasillobox(models.Model):
    idpasillobox = models.AutoField(db_column='idPasilloBox', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45, blank=True, null=True)

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

    class Meta:
        managed = False
        db_table = 'profesional'
class Box(models.Model):
    idbox = models.AutoField(db_column='idBox', primary_key=True)  # Field name made lowercase.
    estadobox_idestadobox = models.ForeignKey('Estadobox', models.DO_NOTHING, db_column='estadoBox_idestadoBox')  # Field name made lowercase.
    numerobox = models.CharField(db_column='numeroBox', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ubicacionbox = models.CharField(db_column='ubicacionBox', max_length=200, blank=True, null=True)  # Field name made lowercase.
    pasillobox_idpasillobox = models.ForeignKey('Pasillobox', models.DO_NOTHING, db_column='pasilloBox_idPasilloBox', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'box'


class Boxprofesional(models.Model):
    idboxprofesionalcol = models.CharField(db_column='idBoxProfesionalcol', primary_key=True, max_length=45)  # Field name made lowercase.
    box_idbox = models.ForeignKey(Box, models.DO_NOTHING, db_column='Box_idBox')  # Field name made lowercase.
    profesional_idprofesional = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='Profesional_idProfesional')  # Field name made lowercase.
    fechaasignacion = models.DateField(db_column='fechaAsignacion', blank=True, null=True)  # Field name made lowercase.
    fechatermino = models.DateField(db_column='fechaTermino', blank=True, null=True)  # Field name made lowercase.
    horarioinicio = models.TimeField(db_column='horarioInicio', blank=True, null=True)  # Field name made lowercase.
    horariofin = models.TimeField(db_column='horarioFin', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'boxprofesional'
