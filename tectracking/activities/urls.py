from django.conf.urls.defaults import *
from tectracking.activities.views import ActivityListView, CalendarView

urlpatterns = patterns(
    '',
    (r'^$', ActivityListView.as_view()),
    (r'^calendar/$', CalendarView.as_view()),
)

