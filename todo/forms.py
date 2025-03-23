from datetime import datetime

from django import forms
from django_summernote.widgets import SummernoteWidget

from todo.models import ToDo, Comment


class ToDoPostForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ('title', 'image', 'description', 'start_date', 'end_date', 'is_completed')
        widgets = {
            'description': SummernoteWidget(),
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'start_date' : forms.DateInput(attrs={'class':'form-control', 'type':datetime.date}),
            'end_date' : forms.DateInput(attrs={'class':'form-control', 'type':datetime.date}),
        }

class ToDoUpdateForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ('title', 'image', 'description', 'start_date', 'end_date', 'is_completed')
        widgets = {
            'description': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': datetime.date}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': datetime.date}),
            'is_completed': forms.CheckboxInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
        }

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)
        label = {
            'message':'내용'
        }
        widgets = {
            'message': forms.Textarea(
                attrs={'rows':2, 'cols':10, 'class':'form-control', 'placeholder':'댓글을 입력해주세요.'})
        }
