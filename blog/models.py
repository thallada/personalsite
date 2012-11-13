from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.comments.signals import comment_was_flagged, comment_was_posted
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


class Tag(models.Model):
    name = models.CharField('name', max_length=100)

    def __unicode__(self):
        return self.name


class Entry(models.Model):
    title = models.CharField('entry title', max_length=160, unique=True)
    slug = models.SlugField('slug', max_length=100, unique=True)
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    last_mod = models.DateTimeField('last modified', auto_now=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('detail', None, {'slug': self.slug})

    class Meta:
        verbose_name_plural = 'entries'


class Project(models.Model):
    title = models.CharField('project title', max_length=160)
    desc = models.TextField('description')
    link = models.URLField('link', null=True, blank=True)
    is_finished = models.BooleanField('is project finished')
    done_date = models.DateField('date finished', null=True, blank=True)
    last_mod = models.DateTimeField('last modified', auto_now=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return reverse('projects')+'#project_'+self.id


@receiver(comment_was_posted)
def comment_handler(sender, **kwargs):
    message = "Comment was added to %s by %s: \n\n%s" % (
            kwargs['comment'].content_object.title, kwargs['comment'].user_name,
            kwargs['comment'].comment
    )
    from_addr = "no-reply@hallada.net"
    recipient_list = [settings.ADMINS[0][1]]
    send_mail("New comment added", message, from_addr, recipient_list)

@receiver(comment_was_flagged)
def commentflag_handler(sender, **kwargs):
    message = "Comment by %s on %s was flagged: \n\n%s" % (
            kwargs['comment'].user_name, kwargs['comment'].content_object.title,
            kwargs['comment'].comment
    )
    from_addr = "no-reply@hallada.net"
    recipient_list = [settings.ADMINS[0][1]]
    send_mail("New comment added", message, from_addr, recipient_list)
