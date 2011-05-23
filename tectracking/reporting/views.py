from tectracking.activities.models import Activity
from tectracking.inventory.models import Asset
from django.views.generic.list import ListView

class ActivityReportingView(ListView):
    model = Activity
    template_name = 'reporting/activities.html'

class InventoryReportingView(ListView):
    model = Asset
    template_name = 'reporting/inventory.html'
