from models import Activity, ActivityTask, Note
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from tectracking.activities.models import Assignment
from django.utils.datastructures import DotExpandedDict
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect

class CalendarView(TemplateView):
    template_name = 'calendar.html'

class ActivityListView(ListView):
    model = Activity

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated():
            assignments = Assignment.objects.filter(user=self.request.user)
        else:
            assignments = None

        if self.request.user.has_perm('activities.can_accept_activity'):
            unassigned_activities = Activity.objects.filter(status='N')
            users = User.objects.filter(is_active='Y')
        else:
            unassigned_activities = None
            users = None

        context = {
            'assignments': assignments,
            'unassigned_activities': unassigned_activities,
            'users': users,
        }
        kwargs.update(context)
        return super(ActivityListView, self).get_context_data(**kwargs)

class ActivityDetailView(DetailView):
    model = Activity

    def get_context_data(self, **kwargs):
        priority_choices = Assignment.PRIORITY_CHOICES

        notes = Note.objects.filter(activity=self.object)

        try:
            assignment = self.object.assignment
        except Assignment.DoesNotExist:
            assignment = None


        if self.request.user.has_perm('activities.can_accept_activity'):
            users = User.objects.filter(is_active='Y')
        else:
            users = None

        context = {
            'users': users,
            'assignment': assignment,
            'notes': notes,
            'priority_choices': priority_choices,
        }

        kwargs.update(context)
        return super(ActivityDetailView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        errors = []
        messages = []
        dotdict = DotExpandedDict(request.POST)

        self.object = self.get_object()

        if self.request.user.is_authenticated():
            if dotdict.get('assignment', ''):
                if self.request.user.has_perm('activities.can_accept_activity'):
                    try:
                        assignment = Assignment.objects.get(activity=self.object)
                    except Assignment.DoesNotExist:
                        assignment = Assignment(activity=self.object)

                    user = dotdict['assignment'].get('user', '')
                    if user:
                        try:
                            assignment.user = User.objects.get(pk=int(user))
                        except (User.DoesNotExist, ValueError):
                            errors.append('User with id %s does not exist.' % user)
                    elif not assignment.user:
                        errors.append('You must assign a user to an activity.')

                    priority = dotdict['assignment'].get('priority', '')
                    if priority:
                        try:
                            assignment.priority = int(priority)
                        except ValueError:
                            errors.append('Priority must be an integer.')
                    elif not assignment.priority:
                        errors.append('You must assign a priority to an activity.')

                    escalation_status = dotdict['assignment'].get('escalation_status', '')
                    if escalation_status:
                        assignment.escalation_status = escalation_status

                    if not errors:
                        try:
                            assignment.full_clean()
                            assignment.save()

                            if self.object.status == 'N':
                                self.object.status = 'A'
                                self.object.save()
                        except ValidationError, e:
                            for key, value in e.message_dict:
                                errors.append(value)
                else:
                    errors.append('You do not have permission to assign a user to an activity.')

            approved_id = dotdict.get('approved_id', '').strip()
            if approved_id:
                if self.request.user.has_perm('activities.can_approve_activity') \
                      and self.object.assignment.user == self.request.user \
                      or 'member' in self.request.user.groups.values_list('name', flat=True):
                    if self.object.status == 'A':
                        self.object.status = 'I'
                        self.object.approved_id = approved_id
                        self.object.save()
                    else:
                        errors.append('The activity must be accepted before it can be approved.')
                else:
                    errors.append('You do not have permission to approve an activity.')

            if dotdict.get('note', ''):
                note = Note(activity=self.object)

                message = dotdict['note'].get('message', '').strip()
                if message:
                    note.message = message
                    note.user = self.request.user
                    note.save()
                else:
                    errors.append('Message cannot be empty.')
        else:
            errors.append('You must be logged in to edit an activity.')

        if errors:
            context = self.get_context_data(errors=errors, messages=messages)
            return self.render_to_response(context)
        else:
            return HttpResponseRedirect(self.request.get_full_path())

class ActivityTaskListView(ListView):
    model = ActivityTask

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)

        if pk is not None:
            return ActivityTask.objects.filter(activity__pk=pk)

        return None
