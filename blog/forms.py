from django import forms
from .models import Comment


class IncognitoCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5})
        }


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5})
        }