from django.views.generic.base import TemplateView
from tectracking.common.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class RegisterView(TemplateView):
    template_name = 'auth/register.html'

    def get_context_data(self, **kwargs):
        return {
                'form': kwargs.pop('form', UserCreationForm()),
                'params': kwargs
                }

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(self.request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('register_complete'))
        else:
            context = self.get_context_data(form=form, **kwargs)
            return self.render_to_response(context)

class RegisterCompleteView(TemplateView):
    template_name = 'auth/register_complete.html'

class IndexView(TemplateView):
    template_name = 'base.html'
