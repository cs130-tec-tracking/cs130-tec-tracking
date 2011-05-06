from django.template import Context, loader
from django.http import HttpResponse

# Create your views here.
def calendar(request):
    template = loader.get_template('calendar.html')
    context = Context()
    return HttpResponse(template.render(context))
