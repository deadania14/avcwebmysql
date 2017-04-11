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
    date = forms.DateTimeField(
        widget=forms.DateInput(),
        input_formats = ('%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y', '%Y-%m-%d'),
        required=False,
        label=("Tanggal Latihan"),
        error_messages={
            'invalid': (u'Enter a valid date.'),}
    )
    class Meta:
        model = Practice
        exclude = ('created_date',)
