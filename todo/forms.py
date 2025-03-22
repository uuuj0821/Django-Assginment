from django import forms
from todo.models import ToDo, Comment


class ToDoPostForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')

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
