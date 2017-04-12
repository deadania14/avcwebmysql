from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Article, Practice

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','text',
        'image',)

class SchedulesForm(forms.ModelForm):
            
    class Meta:
        model = Practice
        exclude = ('created_date',)
