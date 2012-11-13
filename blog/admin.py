from blog.models import Entry, Project, Tag
from django.contrib import admin
from django.contrib import comments

class EntryAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'text']
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Entry, EntryAdmin)
admin.site.register(comments.models.CommentFlag)
admin.site.register(Project)
admin.site.register(Tag)
