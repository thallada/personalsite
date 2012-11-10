from django.db import models
from django.contrib.comments import Comment

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
