from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from models import Hall
from django.conf import settings
from django.http import HttpResponse
from os.path import join

SVG_DIR = join(settings.STATIC_ROOT, 'svg')
SVG_URL = join(settings.STATIC_URL, 'svg')

def main_page(request):
    # TODO: Get residence hall from cookies
    return render_to_response('laundry/main.html',
            context_instance=RequestContext(request))

    def ajax_get_current(request, hall):
        hall_obj = get_object_or_404(Hall, pk=hall)
        filename = hall_obj.name + '_current.svg'
        laundry.update(hall_obj, filepath=join(SVG_DIR, filename))
        return HttpResponse(SVG_URL, filename)

