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
    username = forms.CharField(help_text='*tidakboleh spasi', required=True)
    email = forms.CharField(label='', widget = forms.TextInput(attrs= { 'placeholder':'email'}))
    password1 = forms.CharField(label='Password', widget = forms.PasswordInput(attrs= {'placeholder':'password'}))
    password2 = forms.CharField(label='Re-password', widget = forms.PasswordInput(attrs= {'placeholder':'re-password'}))
    class Meta:
        model = User
        fields = ('username', 'email',
        'password1', 'password2',)
    def clean_mail(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("email sudah ada")
        return email
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gender', 'phone', 'address', 'photo')

class AdministrasiForm(forms.ModelForm):
    class Meta:
        model = Administrasi
        fields = ('method',)
