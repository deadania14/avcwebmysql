from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Event, UserProfile
from manajemen.models import Administrasi

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'corporate', 'desc', 'sender', 'phone','email',
        'image', 'attachment', 'event_date']

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text='tidakboleh spasi', required=True)
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email',
        'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gender', 'phone', 'address', 'photo')

class AdministrasiForm(forms.ModelForm):
    class Meta:
        model = Administrasi
        fields = ('method',)
