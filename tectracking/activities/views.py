from models import Activity, ActivityTask
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from tectracking.activities.models import Assignment

class CalendarView(TemplateView):
    template_name = 'calendar.html'

class ActivityListView(ListView):
    model = Activity

    def get_context_data(self, **kwargs):
        activities = Activity.objects.all()

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
            'activities': activities,
        }
        kwargs.update(context)
        return super(ActivityListView, self).get_context_data(**kwargs)

class ActivityDetailView(DetailView):
    model = Activity

class ActivityTaskListView(ListView):
    model = ActivityTask

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)

        if pk is not None:
            return ActivityTask.objects.filter(activity__pk=pk)

        return None
