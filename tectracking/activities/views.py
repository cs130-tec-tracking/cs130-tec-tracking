from models import Activity
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

class CalendarView(TemplateView):
    template_name = 'calendar.html'

class ActivityListView(ListView):
    model = Activity
