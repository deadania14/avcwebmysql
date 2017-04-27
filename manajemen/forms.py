from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Article, Practice, Kelas, PracticeAttendance
from public.models import SettingsVariable, Event

class ArticleForm(forms.ModelForm):
    title = forms.CharField(label='Judul', max_length=100, required=True)
    image = forms.ImageField(label = 'Gambar', required=False)
    class Meta:
        model = Article
        fields = ('title','text',
        'image',)

class MainArticleForm(forms.ModelForm):
    image = forms.ImageField(label = 'Gambar', required=False)
    class Meta:
        model = Article
        fields = ('text',
        'image',)

class SchedulesForm(forms.ModelForm):
    date = forms.DateTimeField(label='Tanggal Latihan', required=True)
    place = forms.CharField(label='Tempat', max_length=100, required=True)

    class Meta:
        model = Practice
        exclude = ('created_date',)

class ClassForm(forms.ModelForm):
    user = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
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

class AVCContactForm(forms.ModelForm):
    address = forms.CharField(label='Alamat', max_length=255, required=True)
    phone1 = forms.CharField(label='Telepon Utama', max_length=20, required=True)
    phone2 = forms.CharField(label='Telepon Bantuan', max_length=20, required=True)
    email = forms.EmailField(label='E-mail', max_length=50, required=True)
    class Meta:
        model = SettingsVariable
        fields = ('value',)

class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'desc', 'image', 'event_date']
