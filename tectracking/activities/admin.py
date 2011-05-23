from django.contrib import admin
from models import Activity, Room, RoomReservation, Task, ActivityTask, Assignment, Note

class RoomReservationInline(admin.StackedInline):
    model = RoomReservation
    extra = 1

class RoomReservationTabularInline(admin.TabularInline):
    model = RoomReservation
    extra = 1

class ActivityTaskInline(admin.TabularInline):
    model = ActivityTask

class AssignmentInline(admin.StackedInline):
    model = Assignment
    max_num = 1

class NoteInline(admin.TabularInline):
    model = Note
    extra = 1

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('tec_id', 'event_type', 'short_desc', 'event_start_date', 'siebel_num', 'num_attendees',)
    list_filter = ('assignment__user', 'event_type', 'tec_site', 'num_attendees', 'room_required', 'laptops_required',)
    search_fields = ('assignment__user__first_name', 'assignment__user__last_name', 'siebel_num', 'event_organizer', 'event_type', 'tec_site',)
    inlines = (AssignmentInline, ActivityTaskInline, NoteInline, RoomReservationInline,)
    date_hierarchy = 'event_start_date'

class RoomAdmin(admin.ModelAdmin):
    list_display = ('location', 'capacity', 'num_workstations',)
    list_filter = ('capacity', 'num_workstations',)
    search_fields = ('location',)
    inlines = (RoomReservationTabularInline,)

class RoomReservationAdmin(admin.ModelAdmin):
    list_display = ('activity', 'room', 'datetime', 'duration',)
    list_filter = ('room', 'datetime', 'duration',)
    search_fields = ('activity__tec_id', 'room__location',)
    date_hierarchy = 'datetime'

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (ActivityTaskInline,)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('activity', 'user', 'priority', 'escalation_status',)
    list_filter = ('user', 'priority',)
    search_fields = ('user__first_name', 'user__last_name', 'activity__tec_id',)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('activity', 'user', 'message',)
    list_filter = ('user',)
    search_fields = ('user__first_name', 'user__last_name', 'activity__tec_id',)

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomReservation, RoomReservationAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Note, NoteAdmin)
