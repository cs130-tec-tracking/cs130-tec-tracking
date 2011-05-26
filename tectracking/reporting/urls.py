from django.conf.urls.defaults import patterns, url
from django.views.generic.base import RedirectView
from tectracking.reporting.views import ActivityReportingView, InventoryReportingView, TaskReportingView
from tectracking.utils import reverse_lazy

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('reporting_activity')), name='reporting'),
    url(r'^activities/$', ActivityReportingView.as_view(), name='reporting_activity'),
    url(r'^tasks/$', TaskReportingView.as_view(), name='reporting_tasks'),
    url(r'^inventory/$', InventoryReportingView.as_view(), name='reporting_inventory'),
)
