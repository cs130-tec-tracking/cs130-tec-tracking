from models import Asset, AssetCategory, Note
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.datastructures import DotExpandedDict
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect

class InventoryListView(ListView):
    model = Asset

    def get_context_data(self, **kwargs):
	disp_inventory = Asset.objects.filter()

        context = {
            'disp_inventory': disp_inventory,
        }
        kwargs.update(context)
        return super(InventoryListView, self).get_context_data(**kwargs)

