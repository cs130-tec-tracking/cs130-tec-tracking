from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    REQUIRED_CHOICES = (
        (u'Y', u'Yes'),
        (u'N', u'No'),
    )

    STATUS_CHOICES = (
        (u'N', u'Not Accepted'),
        (u'A', u'Accepted'),
        (u'I', u'Incomplete'),
        (u'C', u'Complete'),
    )

    tec_id = models.CharField(max_length=11, primary_key=True)
    approved_id = models.CharField(max_length=11, blank=True, null=True)
    event_type = models.CharField(max_length=10)
    short_desc = models.CharField(max_length=60, verbose_name='short description')
    reservation_desc = models.CharField(max_length=300, verbose_name='reservation description')
    tec_site = models.CharField(max_length=60)
    event_location = models.CharField(max_length=60)
    event_start_date = models.DateField()
    event_end_date = models.DateField()
    event_organizer = models.CharField(max_length=60)
    date_entered = models.DateField()
    date_last_mod = models.DateField(null=True, blank=True, verbose_name='date last modified')
    event_size = models.IntegerField(null=True, blank=True)
    sponsor_mgr = models.CharField(max_length=60, null=True, blank=True, verbose_name='sponsor manager')
    class_mgr = models.CharField(max_length=60, verbose_name='class manager')
    siebel_num = models.CharField(max_length=9, null=True, blank=True, db_column='siebel_no', verbose_name='siebel number')
    num_attendees = models.IntegerField(db_column='no_attendees', verbose_name='number of attendees')
    room_required = models.CharField(max_length=1, choices=REQUIRED_CHOICES)
    laptops_required = models.CharField(max_length=1, choices=REQUIRED_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')

    reserved_rooms = models.ManyToManyField('Room', through='RoomReservation')
    tasks = models.ManyToManyField('Task', through='ActivityTask')

    class Meta:
        db_table = 'tracking_source'
        verbose_name_plural = 'activities'
        ordering = ['-event_start_date', '-event_end_date']
        permissions = (
            ('can_approve_activity', 'Can approve an activity by settings its approved id'),
            ('can_accept_activity', 'Can accept an activity by settings its status to accepted'),
            ('can_close_activity', 'Can close an activity by settings its status to complete'),
        )

    def __unicode__(self):
        return self.tec_id

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=300)
    capacity = models.IntegerField()
    num_workstations = models.IntegerField(null=True, blank=True, db_column='no_workstations', verbose_name='number of worksations')

    class Meta:
        db_table = 'room'

    def __unicode__(self):
        return self.location

class RoomReservation(models.Model):
    activity = models.ForeignKey(Activity, db_column='tec_id')
    room = models.ForeignKey(Room)
    datetime = models.DateTimeField(verbose_name='time')
    duration = models.TimeField()

    class Meta:
        db_table = 'room_reservations'
        ordering = ['-datetime', '-duration']

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'task'

    def __unicode__(self):
        return self.name

class ActivityTask(models.Model):
    activity = models.ForeignKey(Activity, db_column='tec_id')
    task = models.ForeignKey(Task)
    status = models.CharField(max_length=300, null=True, blank=True)
    assigned_user = models.ForeignKey(User, db_column='auth_user_id', null=True, blank=True, verbose_name='assigned to')

    class Meta:
        db_table = 'activity_tasks'
        permissions = (
            ('can_change_task_status', 'Can change the status of a task'),
        )

class Assignment(models.Model):
    PRIORITY_CHOICES = (
        (1, u'High Priority'),
        (2, u'Normal Priority'),
        (3, u'Low Priority'),
    )

    activity = models.OneToOneField(Activity, db_column='tec_id')
    user = models.ForeignKey(User, db_column='auth_user_id')
    priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=2)
    escalation_status = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'activity_assignments'
        ordering = ['priority']

class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activity, db_column='tec_id')
    user = models.ForeignKey(User, db_column='auth_user_id')
    message = models.TextField()

    class Meta:
        db_table = 'activity_note'
