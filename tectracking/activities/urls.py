from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'^calendar', 'activities.views.calendar'),
)

