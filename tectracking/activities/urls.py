from django.conf.urls.defaults import *
from tectracking.activities.views import ActivityListView, ActivityDetailView, CalendarView, \
    ActivityTaskListView

urlpatterns = patterns(
    '',
    (r'^$', ActivityListView.as_view()),
    (r'^calendar/$', CalendarView.as_view()),
    (r'^(?P<pk>.{11})/$', ActivityDetailView.as_view()),
    (r'^(?P<pk>.{11})/tasks/$', ActivityTaskListView.as_view())
)

