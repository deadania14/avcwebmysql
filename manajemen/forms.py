from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminTimeWidget, AdminSplitDateTime
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from .models import Article, Practice, Kelas, PracticeAttendance, Inventory, Meeting
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
    # date = forms.DateTimeField(label='Tanggal Latihan', required=True)
    date = forms.SplitDateTimeField(label='Tanggal Latihan', required=True, widget=AdminSplitDateTime)
    # time = forms.TimeField(widget=AdminTimeWidget())
    place = forms.CharField(label='Tempat', max_length=100, required=True)

    class Meta:
        model = Practice
        exclude = ('created_date',)

class ClassForm(forms.ModelForm):
    user = AutoCompleteSelectMultipleField(
        'users', required=False, help_text=None
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
    daftar_orang = AutoCompleteSelectMultipleField(
        'users', required=False, help_text=None
    )
    class Meta:
        model = PracticeAttendance
        fields = ("daftar_orang",'practice','tutor',)

class AVCContactForm(forms.Form):
    address = forms.CharField(label='Alamat', max_length=255, required=True)
    phone1 = forms.CharField(label='Telepon Utama', max_length=20, required=True)
    phone2 = forms.CharField(label='Telepon Bantuan', max_length=20, required=True)
    email = forms.EmailField(label='E-mail', max_length=50, required=True)
    facebook = forms.CharField(label='Facebook', max_length=100, required=True)
    twitter = forms.CharField(label='Twitter', max_length=100, required=True)
    instagram = forms.CharField(label='Instagram', max_length=100, required=True)
    youtube = forms.CharField(label='Youtube', max_length=100, required=True)

class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'desc', 'image', 'event_date',]

class EditBarangForm(forms.ModelForm):
    class Meta:
        model = Inventory
        exclude = ('created_date','updated_date',)

class NewNoteMeet(forms.ModelForm):
    title = forms.CharField(label='Judul', max_length=100, required=True)
    note = forms.CharField(label='Catatan', required=True)
    class Meta:
        model = Meeting
        exclude =('created_date', 'updated_date',)

class EditNoteMeet(forms.ModelForm):

    class Meta:
         model = Meeting
         exclude = ('title',)
