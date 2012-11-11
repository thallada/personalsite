from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from blog.models import Entry
from django.contrib.comments import Comment
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import json
import markdown_deux

DEFAULT_INDEX_NUM = getattr(settings, 'DEFAULT_INDEX_NUM', 5)
MONTHS = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
        6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October',
        11: 'November', 12: 'December'}


def get_entries(num=DEFAULT_INDEX_NUM, order_by='-pub_date'):
    # Get all the latest entries by default or 'num' entries posted
    # ordered by 'order_by'. Entries are sanitized.
    entries = Entry.objects.all().order_by(order_by)
    if num:
        entries = entries[:int(num)]
    return entries


def index(request):
    # User can request a different number of entries to show in the index
    num = request.GET.get('num', DEFAULT_INDEX_NUM)
    order_by = request.GET.get('order_by', '-pub_date')
    entries = get_entries(num=num, order_by=order_by)
    return render_to_response('blog/index.html', {'latest_entries': entries})


def detail(request, entry_id):
    # Show one specific entry including comments
    e = get_object_or_404(Entry, pk=entry_id)
    c = Comment.objects.filter(object_pk=entry_id)
    return render_to_response('blog/detail.html', {'entry': e, 'comments': c,
            'next': e.get_absolute_url()},
            context_instance=RequestContext(request))


def archive(request):
    # Show all comments sorted by date descending.
    entries = [(e.pub_date.strftime('%b %d, %Y'), e)
            for e in get_entries(num=0)]
    return render_to_response('blog/archive.html',
            {'entries': entries})


def about(request):
    # Return about me page.
    return render_to_response('blog/about.html', {})


@require_POST
def markdown_comment(request):
    # Exclusively for ajax posts. Return a user's comment in markdown converted
    # to safe html for posting.
    if request.is_ajax():
        return HttpResponse(json.dumps({
            'comment': markdown_deux.markdown(request.POST.get('comment', '')),
        }, ensure_ascii=False), mimetype='application/javascript')
