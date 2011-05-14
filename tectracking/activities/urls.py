from django.conf.urls.defaults import patterns, url
from tectracking.activities.views import ActivityListView, ActivityDetailView, CalendarView, \
    ActivityTaskListView

urlpatterns = patterns(
    '',
    url(r'^$', ActivityListView.as_view(), name='activities'),
    url(r'^calendar/$', CalendarView.as_view(), name='activity_calendar'),
    url(r'^(?P<pk>.{11})/$', ActivityDetailView.as_view(), name='activity_detail'),
    url(r'^(?P<pk>.{11})/tasks/$', ActivityTaskListView.as_view(), name='activity_task_list'),
)
