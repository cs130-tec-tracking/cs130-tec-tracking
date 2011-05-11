from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import RedirectView
from tectracking.common.views import IndexView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/index')),
    url(r'^index/$', IndexView.as_view()),
    url(r'^activities/', include('tectracking.activities.urls')),
    url(r'^inventory/', include('tectracking.inventory.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
