# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
# Unable to inspect table 'afghanistan_population'
# The error was: permission denied for relation afghanistan_population



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
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
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
# Unable to inspect table 'bangladesh_population'
# The error was: permission denied for relation bangladesh_population

# Unable to inspect table 'belize_population'
# The error was: permission denied for relation belize_population

# Unable to inspect table 'bolivia_population'
# The error was: permission denied for relation bolivia_population



class BooksAuthor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'books_author'


class BooksBook(models.Model):
    title = models.CharField(max_length=100)
    publication_date = models.DateField(blank=True, null=True)
    publisher = models.ForeignKey('BooksPublisher', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_book'


class BooksBookAuthors(models.Model):
    book = models.ForeignKey(BooksBook, models.DO_NOTHING)
    author = models.ForeignKey(BooksAuthor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_book_authors'
        unique_together = (('book', 'author'),)


class BooksPublisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'books_publisher'
# Unable to inspect table 'burkina_faso_population'
# The error was: permission denied for relation burkina_faso_population

# Unable to inspect table 'burundi_population'
# The error was: permission denied for relation burundi_population

# Unable to inspect table 'cambodia_population'
# The error was: permission denied for relation cambodia_population



class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
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
# Unable to inspect table 'gambia_population'
# The error was: permission denied for relation gambia_population



class MusicWater(models.Model):
    row_id = models.TextField(blank=True, null=True)
    country_name = models.TextField(blank=True, null=True)
    water_source = models.TextField(blank=True, null=True)
    water_tech = models.TextField(blank=True, null=True)
    status_id = models.TextField(blank=True, null=True)
    managment = models.TextField(blank=True, null=True)
    pay = models.TextField(blank=True, null=True)
    installer = models.TextField(blank=True, null=True)
    install_year = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    adm1 = models.TextField(blank=True, null=True)
    adm2 = models.TextField(blank=True, null=True)
    wpdx_id = models.TextField(blank=True, null=True)
    report_date = models.TextField(blank=True, null=True)
    country_id = models.TextField(blank=True, null=True)
    activity_id = models.TextField(blank=True, null=True)
    data_lnk = models.TextField(blank=True, null=True)
    org_lnk = models.TextField(blank=True, null=True)
    photo_lnk = models.TextField(blank=True, null=True)
    converted = models.TextField(blank=True, null=True)
    created = models.TextField(blank=True, null=True)
    updated = models.TextField(blank=True, null=True)
    lat_deg = models.TextField(blank=True, null=True)
    lon_deg = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    count = models.TextField(blank=True, null=True)
    fecal_coliform_presence = models.TextField(blank=True, null=True)
    fecal_coliform_value = models.TextField(blank=True, null=True)
    subjective_quality = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'music_water'
# Unable to inspect table 'newtable'
# The error was: permission denied for relation newtable


class SwaziMvp(models.Model):
    id = models.TextField(primary_key = True, db_column="id")
    country_name = models.TextField(db_column = "country_name", blank = True, null = True)
    water_source = models.TextField(db_column='water_source', blank=True, null=True)
    water_tech = models.TextField(db_column='water_tech', blank=True, null=True)
    status_id= models.TextField(db_column='status_id', blank=True, null=True)
    install_year = models.TextField(db_column='install_year', blank=True, null=True)
    lat_deg = models.TextField(db_column='lat_deg', blank=True, null=True)
    lon_deg = models.TextField(db_column='lon_deg', blank=True, null=True)
    fuzzy_water_source = models.TextField(db_column='fuzzy_water_source', blank=True, null=True)
    predicted_class = models.TextField(db_column='predicted_class', blank=True, null=True)
    probability = models.TextField(db_column='probability', blank=True, null=True)
    one_km_population = models.TextField(db_column='one_km_population', blank=True, null=True)
    one_km_total_water_points = models.TextField(db_column='one_km_total_water_points', blank=True, null=True)
    one_km_functioning_water_points = models.TextField(db_column='one_km_functioning_water_points', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'swazi_mvp'

class SwaziTest(models.Model):
    id = models.TextField(primary_key=True)
    row_id = models.TextField(db_column='Row ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    field_country_name = models.TextField(db_column='#country_name', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_water_source = models.TextField(db_column='#water_source', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_water_tech = models.TextField(db_column='#water_tech', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_status_id = models.TextField(db_column='#status_id', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_management = models.TextField(db_column='#management', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_pay = models.TextField(db_column='#pay', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_installer = models.TextField(db_column='#installer', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_install_year = models.TextField(db_column='#install_year', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_status = models.TextField(db_column='#status', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_source = models.TextField(db_column='#source', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_adm1 = models.TextField(db_column='#adm1', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_adm2 = models.TextField(db_column='#adm2', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_wpdx_id = models.TextField(db_column='#wpdx_id', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_report_date = models.TextField(db_column='#report_date', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_country_id = models.TextField(db_column='#country_id', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_activity_id = models.TextField(db_column='#activity_id', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_data_link = models.TextField(db_column='#data_link', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_orig_lnk = models.TextField(db_column='#orig_lnk', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    photo_lnk = models.TextField(blank=True, null=True)
    field_converted = models.TextField(db_column='#converted', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_created = models.TextField(db_column='#created', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_updated = models.TextField(db_column='#updated', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_lat_deg = models.FloatField(db_column='#lat_deg', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_long_deg = models.FloatField(db_column='#long_deg', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.
    count = models.TextField(db_column='Count', blank=True, null=True)  # Field name made lowercase.
    field_fecal_coliform_presence = models.TextField(db_column='#fecal_coliform_presence', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_fecal_coliform_value = models.TextField(db_column='#fecal_coliform_value', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_subjective_quality = models.TextField(db_column='#subjective_quality', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    number_1_km_population = models.TextField(db_column='1 km population', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = 'swazi_test'





class Water(models.Model):
    row_id = models.TextField(blank=True, null=True)
    country_name = models.TextField(blank=True, null=True)
    water_source = models.TextField(blank=True, null=True)
    water_tech = models.TextField(blank=True, null=True)
    status_id = models.TextField(blank=True, null=True)
    management = models.TextField(blank=True, null=True)
    pay = models.TextField(blank=True, null=True)
    installer = models.TextField(blank=True, null=True)
    install_year = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    adm1 = models.TextField(blank=True, null=True)
    adm2 = models.TextField(blank=True, null=True)
    wpdx_id = models.TextField(blank=True, null=True)
    report_date = models.TextField(blank=True, null=True)
    country_id = models.TextField(blank=True, null=True)
    activity_id = models.TextField(blank=True, null=True)
    data_lnk = models.TextField(blank=True, null=True)
    org_lnk = models.TextField(blank=True, null=True)
    photo_lnk = models.TextField(blank=True, null=True)
    converted = models.TextField(blank=True, null=True)
    created = models.TextField(blank=True, null=True)
    updated = models.TextField(blank=True, null=True)
    lat_deg = models.TextField(blank=True, null=True)
    lon_deg = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    count = models.TextField(blank=True, null=True)
    fecal_coliform_presence = models.TextField(blank=True, null=True)
    fecal_coliform_value = models.TextField(blank=True, null=True)
    subjective_quality = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'water'


class WaterDjango(models.Model):
    row_id = models.TextField(blank=True, null=True)
    country_name = models.TextField(blank=True, null=True)
    water_source = models.TextField(blank=True, null=True)
    water_tech = models.TextField(blank=True, null=True)
    status_id = models.TextField(blank=True, null=True)
    management = models.TextField(blank=True, null=True)
    pay = models.TextField(blank=True, null=True)
    installer = models.TextField(blank=True, null=True)
    install_year = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    adm1 = models.TextField(blank=True, null=True)
    adm2 = models.TextField(blank=True, null=True)
    wpdx_id = models.TextField(blank=True, null=True)
    report_date = models.TextField(blank=True, null=True)
    country_id = models.TextField(blank=True, null=True)
    activity_id = models.TextField(blank=True, null=True)
    data_lnk = models.TextField(blank=True, null=True)
    org_lnk = models.TextField(blank=True, null=True)
    photo_lnk = models.TextField(blank=True, null=True)
    converted = models.TextField(blank=True, null=True)
    created = models.TextField(blank=True, null=True)
    updated = models.TextField(blank=True, null=True)
    lat_deg = models.TextField(blank=True, null=True)
    lon_deg = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    count1 = models.TextField(blank=True, null=True)
    fecal_coliform_presence = models.TextField(blank=True, null=True)
    fecal_coliform_value = models.TextField(blank=True, null=True)
    subjective_quality = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'water_django'
