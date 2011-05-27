from django.contrib import admin
from models import Activity, Task, ActivityTask, Assignment, Note
from tectracking.inventory.models import AssetReservation

class AssetReservationInline(admin.StackedInline):
    model = AssetReservation
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
    list_display = ('tec_id', 'approved_id', 'event_type', 'short_desc', 'event_start_date', 'siebel_num', 'num_attendees', 'status',)
    list_filter = ('assignment__user', 'event_type', 'tec_site', 'num_attendees', 'room_required', 'laptops_required', 'status',)
    search_fields = ('tec_id', 'approved_id', 'assignment__user__first_name', 'assignment__user__last_name', 'siebel_num', 'event_organizer', 'event_type', 'tec_site',)
    inlines = (AssignmentInline, ActivityTaskInline, NoteInline, AssetReservationInline,)
    date_hierarchy = 'event_start_date'

class ActivityTaskAdmin(admin.ModelAdmin):
    list_display = ('activity', 'task', 'status', 'assigned_user',)
    list_filter = ('assigned_user',)
    search_fields = ('assigned__user__first_name', 'assigned_user__last_name', 'task__name', 'activity__tec_id', 'activity__approved_id', 'activity__siebel_num',)

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
admin.site.register(ActivityTask, ActivityTaskAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Note, NoteAdmin)
