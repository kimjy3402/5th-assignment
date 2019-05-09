from django import forms
from .models import Blog, Comment #추가된 부분

class BlogPost(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body']

#추가된 부분
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']