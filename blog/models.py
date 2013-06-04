from django.db import models
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy, reverse
import markdown_deux
from django.contrib.comments.signals import comment_was_flagged
from django.contrib.comments.signals import comment_was_posted
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.sites.models import get_current_site
import datetime


class Tag(models.Model):
    name = models.CharField('name', max_length=100)

    def __unicode__(self):
        return self.name


class EntryManager(models.Manager):
    def public(self):
        return super(EntryManager, self).all().filter(
                pub_date__isnull=False)


class Entry(models.Model):
    title = models.CharField('entry title', max_length=160, unique=True)
    slug = models.SlugField('slug', max_length=100, unique=True)
    text = models.TextField()
    pub_date = models.DateTimeField('date published', null=True, blank=True)
    last_mod = models.DateTimeField('last modified', auto_now=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    objects = EntryManager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('detail', None, {'slug': self.slug})

    def publish(self):
        if not self.pub_date:
            self.pub_date = datetime.datetime.now()

    def unpublish(self):
        if self.pub_date:
            self.pub_date = None

    def _is_published(self):
        return bool(self.pub_date)

    published = property(_is_published)

    class Meta:
        verbose_name_plural = 'entries'


class EntriesFeed(Feed):
    feed_type = Rss201rev2Feed
    title = "Tyler Hallada"
    link = reverse_lazy('rss')
    description = "List of latest blog entries from Tyler Hallada's blog at " \
            "hallada.net."

    def items(self):
        return Entry.objects.order_by('-pub_date')[:10]

    def item_description(self, item):
        return markdown_deux.markdown(item.text, style='post_style')


class Project(models.Model):
    title = models.CharField('project title', max_length=160)
    desc = models.TextField('description')
    link = models.URLField('link', null=True, blank=True)
    img_link = models.URLField('image link', null=True, blank=True)
    is_finished = models.BooleanField('is project finished')
    done_date = models.DateField('date finished', null=True, blank=True)
    last_mod = models.DateTimeField('last modified', auto_now=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return reverse_lazy('projects') + '#project_' + self.id


@receiver(comment_was_posted)
def comment_handler(sender, **kwargs):
    domain = 'http://' + get_current_site(kwargs['request']).domain
    title = "[hallada.net] Comment was added to \"%s\" by %s" % (
            kwargs['comment'].content_object.title,
            kwargs['comment'].user_name,
    )
    message = "View comment: %s%s | Edit comment: %s%s\n\n%s" % (
            domain, kwargs['comment'].get_absolute_url(),
            domain, reverse('admin:comments_comment_change',
                    args=(kwargs['comment'].id,)),
            kwargs['comment'].comment
    )
    from_addr = "no-reply@hallada.net"
    recipient_list = [settings.ADMINS[0][1]]
    send_mail(title, message, from_addr, recipient_list)


@receiver(comment_was_flagged)
def commentflag_handler(sender, **kwargs):
    domain = 'http://' + get_current_site(kwargs['request']).domain
    title = "[hallada.net] Comment by %s on \"%s\" was flagged" % (
            kwargs['comment'].user_name,
            kwargs['comment'].content_object.title,
    )
    message = "View comment: %s%s | Edit comment: %s%s | " \
            "Edit flag: %s%s\n\n%s" % (
            domain, kwargs['comment'].get_absolute_url(),
            domain, reverse('admin:comments_comment_change',
                    args=(kwargs['comment'].id,)),
            domain, reverse('admin:comments_commentflag_change',
                    args=(kwargs['flag'].id,)),
            kwargs['comment'].comment
    )
    from_addr = "no-reply@hallada.net"
    recipient_list = [settings.ADMINS[0][1]]
    send_mail(title, message, from_addr, recipient_list)
