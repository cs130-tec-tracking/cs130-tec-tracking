from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='inventory'),
)
