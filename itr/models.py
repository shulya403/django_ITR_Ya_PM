import datetime

from django.db import models
from django.utils import timezone


# Create your models here.


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
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


class Mnt(models.Model):

    discription = 'Мониторы'

    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=200)  # Field name made lowercase.
    screen_size = models.CharField(db_column='Screen_size', max_length=45, blank=True, null=True, verbose_name=u'Размер экрана')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mnt'


class Nb(models.Model):

    discription = 'Ноутбуки'

    name = models.CharField(db_column='Name', primary_key=True, max_length=200)  # Field name made lowercase.
    screen_size = models.CharField(db_column='Screen_size', max_length=45, blank=True, null=True, verbose_name=u'Размер экрана')  # Field name made lowercase.
    video_conf = models.CharField(db_column='Video_conf', max_length=45, blank=True, null=True, verbose_name=u'Класс GPU')  # Field name made lowercase.
    clusters_screen_gpu = models.CharField(db_column='Clusters_screen_gpu', max_length=45, blank=True, null=True, verbose_name=u'Кластер экран/GPU')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nb'

class Prices(models.Model):

    cat_runame = (
        ('NB', 'Ноутбук'),
        ('MNT', 'Монитор'),
    )

    avg_price = models.IntegerField(db_column='Avg_price', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=3, blank=True, null=True, choices=cat_runame)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    quantaty = models.IntegerField(db_column='Quantaty', blank=True, null=True)  # Field name made lowercase.
    vendor = models.CharField(db_column='Vendor', max_length=45, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=200)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    #name = models.ForeignKey('Nb', on_delete='DO_NOTHING', to_field='name')
    #name = models.ForeignKey('Mnt', on_delete='DO_NOTHING', to_field='name')

    class Meta:
        managed = False
        db_table = 'prices'

dict_models = {
    'Мониторы': Mnt,
    'Ноутбуки': Nb}