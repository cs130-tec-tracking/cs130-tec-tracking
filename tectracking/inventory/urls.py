from django.conf.urls.defaults import patterns, url
from tectracking.inventory.views import InventoryListView

urlpatterns = patterns(
    '',
    url(r'^$', InventoryListView.as_view(), name='inventory'),
)
