from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'^$', 'activities.views.list'),
    (r'^calendar', 'activities.views.calendar'),
)

