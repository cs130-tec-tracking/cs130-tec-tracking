from models import Activity, ActivityTask, Note
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from tectracking.activities.models import Assignment
from django.utils.datastructures import DotExpandedDict
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib import messages

class CalendarView(TemplateView):
    template_name = 'calendar.html'

class ActivityListView(ListView):
    model = Activity

    def get_context_data(self, **kwargs):
        priority_choices = Assignment.PRIORITY_CHOICES

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
            'priority_choices': priority_choices,
        }
        kwargs.update(context)
        return super(ActivityListView, self).get_context_data(**kwargs)

class ActivityDetailView(DetailView):
    model = Activity

    def get_context_data(self, **kwargs):
        priority_choices = Assignment.PRIORITY_CHOICES

        notes = Note.objects.filter(activity=self.object)
        activity_tasks = ActivityTask.objects.filter(activity=self.object)

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
            'activity_tasks': activity_tasks,
            'priority_choices': priority_choices,
        }

        kwargs.update(context)
        return super(ActivityDetailView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        error = False
        dotdict = DotExpandedDict(request.POST)

        self.object = self.get_object()

        if self.request.user.is_authenticated():
            if dotdict.has_key('assignment') and self.object.status == 'C':
                messages.error(self.request, 'You cannot change the assignment of a closed activity.')
                error = True
            elif dotdict.get('assignment', ''):
                user_id = dotdict['assignment'].get('user', '')
                priority = dotdict['assignment'].get('priority', '')
                escalation_status = dotdict['assignment'].get('escalation_status', '')
                user = None

                if user_id:
                    try:
                        user = User.objects.get(pk=int(user_id))
                    except (User.DoesNotExist, ValueError):
                        messages.error(self.request, 'User with id %s does not exist.' % user_id)
                        error = True


                if priority:
                    try:
                        priority = int(priority)
                    except ValueError:
                        messages.error(self.request, 'Priority must be an integer.')
                        error = True

                if not error:
                    error = not self.assign_user(user, priority, escalation_status)

            if dotdict.has_key('approved_id'):
                approved_id = dotdict.get('approved_id', '').strip()
                if self.object.status == 'C':
                    messages.error(self.request, 'You cannot approve a closed activity.')
                    error = True
                elif approved_id and not error:
                    error = not self.approve_activity(approved_id)
                else:
                    messages.error(self.request, 'You must provide an Approved ID.')
                    error = True

            if dotdict.get('note', ''):
                message = dotdict['note'].get('message', '').strip()

                if not error:
                    error = not self.add_note(message, self.request.user)


            status = dotdict.get('status', '')
            if status == 'C':
                if not error:
                    error = not self.close_activity()
        else:
            messages.error(self.request, 'You must be logged in to edit an activity.')
            error = True

        if error:
            context = self.get_context_data()
            return self.render_to_response(context)
        else:
            return HttpResponseRedirect(self.request.get_full_path())

    def user_has_perm(self, perm):
        return self.request.user.has_perm(perm) \
              and (self.object.assignment.user == self.request.user \
              or 'manager' in self.request.user.groups.values_list('name', flat=True))

    def add_note(self, message, user):
        if message:
            note = Note(activity=self.object)
            note.message = message
            note.user = user
            note.save()
            messages.success(self.request, 'Note added successfully.')
            return True
        else:
            messages.error(self.request, 'Message cannot be empty.')
            return False

    def assign_user(self, user, priority, escalation_status):
        if self.request.user.has_perm('activities.can_accept_activity'):
            try:
                assignment = Assignment.objects.get(activity=self.object)
            except Assignment.DoesNotExist:
                assignment = Assignment(activity=self.object)

            if(user is None and not assignment.user):
                messages.error(self.request, 'You must assign a user to an activity.')
                return False

            if(not priority and not assignment.priority):
                messages.error(self.request, 'You must assign a priority to an activity.')
                return False

            assignment.user = user
            assignment.priority = priority

            if escalation_status:
                assignment.escalation_status = escalation_status

            try:
                assignment.full_clean()
                assignment.save()

                if self.object.status == 'N':
                    self.object.status = 'A'
                    self.object.save()
                    messages.success(self.request, 'Acitivity has been accepted.')

                messages.success(self.request, 'Assignment updated successfully.')
                return True
            except ValidationError, e:
                for key, value in e.message_dict:
                    messages.error(self.request, value)
                return False
        else:
            messages.error(self.request, 'You do not have permission to assign a user to an activity.')
            return False

    def approve_activity(self, approved_id):
        if self.user_has_perm('activities.can_approve_activity'):
            if self.object.status == 'A':
                self.object.status = 'I'
                self.object.approved_id = approved_id
                self.object.save()
                messages.success(self.request, 'Activity successfully approved.')
                return True
            else:
                messages.error(self.request, 'The activity must be accepted before it can be approved.')
                return False
        else:
            messages.error(self.request, 'You do not have permission to approve an activity.')
            return False

    def close_activity(self):
        if self.user_has_perm('activities.can_close_activity'):
            if self.object.status == 'I':
                self.object.status = 'C'
                self.object.save()
                messages.success(self.request, 'Activity successfully closed.')
                return True
            else:
                messages.error(self.request, 'The activity must be approved before it can be closed.')
                return False
        else:
            messages.error(self.request, 'You do not have permission to close an activity.')
            return False


class ActivityTaskListView(ListView):
    model = ActivityTask

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)

        if pk is not None:
            return ActivityTask.objects.filter(activity__pk=pk)

        return None
