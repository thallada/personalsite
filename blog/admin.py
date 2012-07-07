from blog.models import Entry
from django.contrib import admin
from django.contrib import comments

class CommentInline(admin.StackedInline):
    model = comments.Comment
    extra = 0

class EntryAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'pub_date']
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_url', 'comment', 'submit_date')
    list_filter = ['submit_date', 'user_name']
    search_fields = ['comment', 'user_name']
    date_hierarchy = 'submit_date'
    
admin.site.register(Entry, EntryAdmin)
