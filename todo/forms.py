from django import forms
from todo.models import ToDo

class ToDoPostForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')

