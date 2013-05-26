from blog.models import Entry, Project, Tag
from django.contrib import admin
from django.contrib import comments
from django import forms

class EntryForm(forms.ModelForm):
    publish = forms.BooleanField(required=False, help_text='Checking this ' \
            'will publish this entry to the blog and set the publish time ' \
            'to the current time. Unchecking will remove the entry from the ' \
            'index and erase any previous publish time.')

    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['text'].help_text = 'Markdown and HTML supported.'

    def save(self, commit=True):
        entry = super(EntryForm, self).save(commit=False)
        if self.cleaned_data['publish']:
            entry.publish()
        else:
            entry.unpublish()
        if commit:
            entry.save()
        return entry

    class Meta:
        model = Entry


class EntryAdmin(admin.ModelAdmin):
    form = EntryForm
    fields = ['title', 'slug', 'text', 'tags', 'publish']
    list_display = ('title', 'published', 'pub_date')
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Entry, EntryAdmin)
admin.site.register(comments.models.CommentFlag)
admin.site.register(Project)
admin.site.register(Tag)
