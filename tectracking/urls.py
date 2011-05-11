from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout, password_reset, password_reset_complete, \
    password_reset_confirm, password_reset_done
from django.views.generic.base import RedirectView
from tectracking.common.views import IndexView, RegisterView, RegisterCompleteView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/index')),
    url(r'^index/$', IndexView.as_view()),
    url(r'^activities/', include('tectracking.activities.urls')),
    url(r'^inventory/', include('tectracking.inventory.urls')),
    url(r'^auth/login/$', login, {'template_name': 'auth/login.html'}),
    url(r'^auth/logout/$', logout, {'next_page': '/index'}),
    url(r'^auth/register/$', RegisterView.as_view(), name='register'),
    url(r'^auth/register/complete/$', RegisterCompleteView.as_view(), name='register_complete'),
    url(r'^auth/reset/$', password_reset, {'template_name': 'auth/password_reset.html',
                                           'email_template_name': 'auth/password_reset_email.html'}),
    url(r'^auth/reset/done/$', password_reset_done, {'template_name': 'auth/password_reset_done.html'}),
    url(r'^auth/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
                                                    {'template_name': 'auth/password_reset_confirm.html'}),
    url(r'^auth/reset/complete/$', password_reset_complete,
                                                    {'template_name': 'auth/password_reset_complete.html'}),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
