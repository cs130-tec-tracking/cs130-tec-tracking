from models import Activity, ActivityTask
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

class CalendarView(TemplateView):
    template_name = 'calendar.html'

class ActivityListView(ListView):
    model = Activity

class ActivityDetailView(DetailView):
    model = Activity

class ActivityTaskListView(ListView):
    model = ActivityTask

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)

        if pk is not None:
            return ActivityTask.objects.filter(activity__pk=pk)

        return None
