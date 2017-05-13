import re
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES
from django.utils.encoding import force_text
from django.forms import ValidationError
from django.forms import Textarea
from django.forms.fields import Field
from django.contrib.auth.models import User
from localflavor.fr.forms import FRPhoneNumberField
from localflavor.generic.forms import DeprecatedPhoneNumberFormFieldMixin
from .models import Event, UserProfile
from manajemen.models import Administrasi

phone_re = re.compile(r'^(\+62|0)[2-9]\d{7,10}$')

class IDPhoneNumberField(Field, DeprecatedPhoneNumberFormFieldMixin):
    """
    An Indonesian telephone number field.

    http://id.wikipedia.org/wiki/Daftar_kode_telepon_di_Indonesia
    """

    default_error_messages = {
        'invalid': _('Enter a valid phone number'),
    }

    def clean(self, value):
        super(IDPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''

        phone_number = re.sub(r'[\-\s\(\)]', '', force_text(value))

        if phone_re.search(phone_number):
            return force_text(value)

        raise ValidationError(self.error_messages['invalid'])

class EventForm(ModelForm):
    event_name = forms.CharField(label='Nama Acara',max_length=50)
    corporate = forms.CharField(label='Instansi', max_length=50)
    desc = forms.CharField(label='Deskripsi Singkat', widget=forms.Textarea)

    sender = forms.CharField(label='Pengaju',max_length=20,)
    phone = IDPhoneNumberField()
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
    last_name = forms.CharField(label='Nama Belakang', help_text='', required=False)
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
    phone = IDPhoneNumberField()
    address = forms.CharField(label='Alamat Domisili', help_text='', required=True)
    class Meta:
        model = UserProfile
        fields = ('gender', 'phone', 'address','photo',)

class AdministrasiForm(forms.ModelForm):
    class Meta:
        model = Administrasi
        fields = ('method',)

class UserProfileEditForm(forms.ModelForm):
    photo = forms.ImageField(label='Foto Profil', help_text='', required=False)
    phone = IDPhoneNumberField()
    address = forms.CharField(label='Alamat Domisili', help_text='', required=True)
    about = forms.CharField(label='Tentang Anda', help_text='pekerjaan, atau kesibukan sehari-hari', required=True)
    class Meta:
        model = UserProfile
        fields = ['phone', 'address','photo', 'about']
