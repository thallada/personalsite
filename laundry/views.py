from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from models import Hall
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from os.path import join
import laundry

SVG_DIR = settings.STATIC_BLOG_ROOT
SVG_URL = settings.STATIC_URL

def main_page(request):
    # pass the halls to the html, and let cookies/user decide which to pick
    halls = [(hall.name, hall.id) for hall in
             Hall.objects.all().order_by('name')]
    return render_to_response('laundry/main.html', {
            'halls': halls,
            },
            context_instance=RequestContext(request))

def ajax_get_current(request, hall):
    hall_obj = get_object_or_404(Hall, pk=hall)
    filename = str(hall_obj.id) + '_current.svg'
    try:
        laundry.update(hall_obj, filepath=join(SVG_DIR, filename))
    except ObjectDoesNotExist:
        raise HttpResponse(status=500);
    return HttpResponse(join(SVG_URL, filename))
