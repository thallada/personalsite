from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from blog.models import Entry
from django.contrib.comments import Comment
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.comments.views.comments import CommentPostBadRequest
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.html import escape
from django.db import models
from django.contrib import comments
from django.contrib.comments import signals
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


def detail(request, entry_id, next=None, using=None):
    # Show one specific entry including comments
    e = get_object_or_404(Entry, pk=entry_id)
    c = Comment.objects.filter(object_pk=entry_id)

    if (request.method == 'POST'):
        # Following code is taken mostly from the django.contrib.comments model,
        # specifically from the post_comment view.

        # Fill out some initial data fields from an authenticated user, if present
        data = request.POST.copy()
        if request.user.is_authenticated():
            if not data.get('name', ''):
                data["name"] = request.user.get_full_name() or request.user.username
            if not data.get('email', ''):
                data["email"] = request.user.email

        # Check to see if the POST data overrides the view's next argument.
        #next = data.get("next", next)

        # Look up the object we're trying to comment about
        ctype = data.get("content_type")
        object_pk = data.get("object_pk")
        if ctype is None or object_pk is None:
            return CommentPostBadRequest("Missing content_type or object_pk field.")
        try:
            model = models.get_model(*ctype.split(".", 1))
            target = model._default_manager.using(using).get(pk=object_pk)
        except TypeError:
            return CommentPostBadRequest(
                "Invalid content_type value: %r" % escape(ctype))
        except AttributeError:
            return CommentPostBadRequest(
                "The given content-type %r does not resolve to a valid model." % \
                    escape(ctype))
        except ObjectDoesNotExist:
            return CommentPostBadRequest(
                "No object matching content-type %r and object PK %r exists." % \
                    (escape(ctype), escape(object_pk)))
        except (ValueError, ValidationError), e:
            return CommentPostBadRequest(
                "Attempting go get content-type %r and object PK %r exists raised %s" % \
                    (escape(ctype), escape(object_pk), e.__class__.__name__))

        # Do we want to preview the comment?
        #preview = "preview" in data

        # Construct the comment form
        form = comments.get_form()(target, data=data)

        # Check security information
        if form.security_errors():
            return CommentPostBadRequest(
                "The comment form failed security verification: %s" % \
                    escape(str(form.security_errors())))

        # If there are errors
        if form.errors:
            return render_to_response(
                'blog/detail.html', {
                    'comment': form.data.get('comment', ''),
                    'form': form,
                    'entry': e,
                },
                context_instance=RequestContext(request)
            )

        # Otherwise create the comment
        comment = form.get_comment_object()
        comment.ip_address = request.META.get("REMOTE_ADDR", None)
        if request.user.is_authenticated():
            comment.user = request.user

        # Signal that the comment is about to be saved
        responses = signals.comment_will_be_posted.send(
            sender  = comment.__class__,
            comment = comment,
            request = request
        )

        for (receiver, response) in responses:
            if response == False:
                return CommentPostBadRequest(
                    "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

        # Save the comment and signal that it was saved
        comment.save()
        signals.comment_was_posted.send(
            sender  = comment.__class__,
            comment = comment,
            request = request
        )

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
