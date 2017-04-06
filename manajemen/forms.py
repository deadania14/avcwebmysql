from django import forms
from django.contrib.auth.models import User
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','text',
        'image',)
