from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from todo.models import ToDo, Comment

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['message', 'author']
    extra = 1

@admin.register(ToDo)
class ToDoAdmin(SummernoteModelAdmin):
    list_display = ['title', 'image', 'description', 'start_date', 'end_date', 'is_completed']
    list_display_links = ['title', 'description']
    list_filter = ['title']
    summernote_fieldsets = ['description', ]
    inlines = [CommentInline]
