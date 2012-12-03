from django.db import models
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
import markdown_deux


class Entry(models.Model):
    title = models.CharField('entry title', max_length=160)
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    last_mod = models.DateTimeField('last modified', auto_now=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('detail', [str(self.id)])

    class Meta:
        verbose_name_plural = 'entries'


class EntriesFeed(Feed):
    title = "Tyler Hallada's latest blog entries"
    link = reverse('rss')
    description = "List of latest blog entries from Tyler Hallada's blog at " \
            "hallada.net."

    def items(self):
        return Entry.objects.order_by('-pub_date')[:10]

    def item_description(self, item):
        return markdown_deux.markdown(item.text, style='post_style')
