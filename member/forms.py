from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from public.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
