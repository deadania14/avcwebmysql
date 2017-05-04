from django.forms import ModelForm
from django import forms
from django.forms import Textarea
from django.contrib.auth.models import User
from .models import Event, UserProfile
from manajemen.models import Administrasi

class EventForm(ModelForm):
    event_name = forms.CharField(label='Nama Acara',max_length=50)
    corporate = forms.CharField(label='Instansi', max_length=50)
    desc = forms.CharField(label='Deskripsi Singkat')
    sender = forms.CharField(label='Pengaju',max_length=20)
    phone = forms.CharField(label='Nomor Handphone',max_length=20)
    email = forms.EmailField(label='E-mail Pengaju',)
    image = forms.ImageField(label='Pamflet atau Poster', required=False,)
    attachment = forms.FileField(label='File Pendukung', help_text='*harus .pdf', required=False)
    event_date = forms.DateField(label='Tanggal Acara', help_text="*Tanggal Kerja Sama")
    class Meta:
        model = Event
        fields = ['event_name', 'corporate', 'desc', 'sender', 'phone','email',
        'image', 'attachment', 'event_date']
        widget = {
             'desc': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

class UserRegister(forms.ModelForm):
    first_name = forms.CharField(label='Nama Depan', help_text='', required=True)
    last_name = forms.CharField(label='Nama Belakang', help_text='', required=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

class UserForm(forms.ModelForm):
    username = forms.CharField(label='Username', help_text='*tidakboleh spasi', required=True)
    email = forms.CharField(label='E-mail', widget = forms.TextInput(attrs= { 'placeholder':'email'}))
    password1 = forms.CharField(label='Password', help_text='*buat password Anda',widget = forms.PasswordInput(attrs= {'placeholder':'password'}))
    password2 = forms.CharField(label='Re-password', widget = forms.PasswordInput(attrs= {'placeholder':'re-password'}))
    class Meta:
        model = User
        fields = ('username', 'email',
        'password1', 'password2',)
    def clean_mail(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("email telah terpakai")
        return email

class UserProfileForm(forms.ModelForm):
    photo = forms.ImageField(label='Foto Profil', help_text='', required=False)
    phone = forms.CharField(label='Nomor Handphone', help_text='', required=True)
    address = forms.CharField(label='Alamat Domisili', help_text='', required=True)
    class Meta:
        model = UserProfile
        fields = ('gender', 'phone', 'address','photo',)

class AdministrasiForm(forms.ModelForm):
    class Meta:
        model = Administrasi
        fields = ('method',)
