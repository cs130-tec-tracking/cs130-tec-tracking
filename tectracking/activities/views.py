from django.template import Context, loader
from django.http import HttpResponse
from models import Activity

def calendar(request):
    template = loader.get_template('calendar.html')
    context = Context()
    return HttpResponse(template.render(context))

def list(request):
    template = loader.get_template('activity_list.html')
    context = Context({
                       'activities': Activity.objects.all()
                       })
    return HttpResponse(template.render(context))
