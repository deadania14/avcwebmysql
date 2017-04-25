from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Article, Practice, Kelas, PracticeAttendance
from public.models import SettingsVariable

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','text',
        'image',)

class SchedulesForm(forms.ModelForm):
    class Meta:
        model = Practice
        exclude = ('created_date',)

class ClassForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = ('nama_kelas','user','note',)

class AbsensiForm(forms.ModelForm):
    is_present = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = PracticeAttendance
        fields = ('is_present', 'tutor_pendamping',)

class AbsensiNewForm(forms.ModelForm):
    class Meta:
        model = PracticeAttendance
        fields = ('kelas','practice','tutor',)

class SettingAVCContacts(forms.ModelForm):
    class Meta:
        model = SettingsVariable
        fields = ('value',)
