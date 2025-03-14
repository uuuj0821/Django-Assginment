from django.contrib import admin
from todo.models import ToDo

@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'start_date', 'end_date', 'is_completed']
    list_display_links = ['title', 'description']
    list_filter = ['title']