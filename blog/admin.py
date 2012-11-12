from blog.models import Entry
from django.contrib import admin
from django.contrib import comments

class EntryAdmin(admin.ModelAdmin):
    fields = ['title', 'text']
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'


admin.site.register(Entry, EntryAdmin)
admin.site.register(comments.models.CommentFlag)
