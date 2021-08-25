# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AppointmentCrons(models.Model):
    appointment_type = models.OneToOneField('AppointmentTypes', models.DO_NOTHING, primary_key=True)
    cron = models.ForeignKey('Crons', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'appointment_crons'
        unique_together = (('appointment_type', 'cron'),)


class AppointmentRoles(models.Model):
    appointment_type = models.OneToOneField('AppointmentTypes', models.DO_NOTHING, primary_key=True)
    role = models.ForeignKey('Roles', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'appointment_roles'
        unique_together = (('appointment_type', 'role'),)


class AppointmentRooms(models.Model):
    appointment_type = models.OneToOneField('AppointmentTypes', models.DO_NOTHING, primary_key=True)
    room = models.ForeignKey('Rooms', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'appointment_rooms'
        unique_together = (('appointment_type', 'room'),)


class AppointmentTypes(models.Model):
    appointment_type_id = models.AutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=254)
    description = models.TextField()
    duration_minutes = models.IntegerField(blank=True, null=True)
    max_participants = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment_types'


class Appointments(models.Model):
    appointment_id = models.BigAutoField(primary_key=True)
    appointment_type = models.ForeignKey(AppointmentTypes, models.DO_NOTHING)
    room = models.ForeignKey('Rooms', models.DO_NOTHING)
    begins_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointments'


class Assignments(models.Model):
    appointment = models.OneToOneField(Appointments, models.DO_NOTHING, primary_key=True)
    assignee = models.ForeignKey('StaffRoles', models.DO_NOTHING)
    assigned_at = models.DateTimeField(blank=True, null=True)
    refused_at = models.DateTimeField(blank=True, null=True)
    changed_at = models.DateTimeField(blank=True, null=True)
    hrate_factor = models.IntegerField(blank=True, null=True)
    work_factor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assignments'
        unique_together = (('appointment', 'assignee'),)


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


class Availabilities(models.Model):
    staff = models.OneToOneField('StaffRoles', models.DO_NOTHING, primary_key=True)
    cron = models.ForeignKey('Crons', models.DO_NOTHING)
    priority = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'availabilities'
        unique_together = (('staff', 'cron'),)


class Bookings(models.Model):
    member = models.OneToOneField('Members', models.DO_NOTHING, primary_key=True)
    appointment = models.ForeignKey(Appointments, models.DO_NOTHING)
    booked_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bookings'
        unique_together = (('member', 'appointment'),)


class Crons(models.Model):
    cron_id = models.AutoField(primary_key=True)
    schedule = models.CharField(unique=True, max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crons'


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


class Invoices(models.Model):
    invoice_id = models.BigAutoField(primary_key=True)
    membership = models.ForeignKey('Memberships', models.DO_NOTHING)
    paydue_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoices'


class Members(models.Model):
    member_id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=254)
    member_name = models.CharField(unique=True, max_length=254)
    password = models.CharField(max_length=254)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'members'


class Memberships(models.Model):
    membership_id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey(Members, models.DO_NOTHING)
    supscription = models.ForeignKey('Supscriptions', models.DO_NOTHING)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'memberships'


class Payrolls(models.Model):
    payroll_id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey(Members, models.DO_NOTHING)
    for_from = models.DateTimeField(blank=True, null=True)
    for_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payrolls'


class Periods(models.Model):
    period_id = models.AutoField(primary_key=True)
    period_name = models.CharField(unique=True, max_length=254)

    class Meta:
        managed = False
        db_table = 'periods'


class Prices(models.Model):
    price_id = models.AutoField(primary_key=True)
    period = models.ForeignKey(Periods, models.DO_NOTHING)
    promotion = models.TextField(blank=True, null=True)
    amount_euro = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prices'


class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=254)
    description = models.TextField(blank=True, null=True)
    hrate_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Rooms(models.Model):
    room_id = models.AutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=254)

    class Meta:
        managed = False
        db_table = 'rooms'


class Specials(models.Model):
    special_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Members, models.DO_NOTHING)
    conditions = models.TextField(blank=True, null=True)
    price_factor = models.IntegerField(blank=True, null=True)
    hrate_factor = models.IntegerField(blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'specials'


class StaffRoles(models.Model):
    staff_id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey(Members, models.DO_NOTHING)
    role = models.ForeignKey(Roles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'staff_roles'


class Supscriptions(models.Model):
    supscription_id = models.AutoField(primary_key=True)
    price = models.ForeignKey(Prices, models.DO_NOTHING)
    title = models.CharField(unique=True, max_length=254)
    description = models.TextField()
    minimum_days = models.IntegerField(blank=True, null=True)
    maximum_days = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supscriptions'


class Transactions(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    invoice_id = models.IntegerField(blank=True, null=True)
    payroll_id = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    amount_euro = models.DecimalField(max_digits=10, decimal_places=2)
    occured_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transactions'
