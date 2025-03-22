from django.contrib import admin
from todo.models import ToDo, Comment

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['message', 'author']
    extra = 1

@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'start_date', 'end_date', 'is_completed']
    list_display_links = ['title', 'description']
    list_filter = ['title']
    inlines = [CommentInline]
