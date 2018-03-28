import re
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES
from django.utils.encoding import force_text
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ValidationError
from django.forms import Textarea
from django.forms.fields import Field
from django.contrib.auth.models import User
from localflavor.fr.forms import FRPhoneNumberField
from localflavor.generic.forms import DeprecatedPhoneNumberFormFieldMixin
from .models import Event, UserProfile, Slider, SettingsVariable
from manajemen.models import Administrasi, PracticeAttendance

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
    event_date= forms.DateField(
        widget=SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        )
    )
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

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nama Depan')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label='Nama Belakang')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone = IDPhoneNumberField()
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'phone', 'email', 'password1', 'password2', )
    def clean_mail(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("email telah terdigunakan")
        return email

class NewPaymentForm(forms.ModelForm):
    class Meta:
        model = Administrasi
        exclude = ['created_date','nominal','status','user',]

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

class RegisterTransferForm(forms.ModelForm):
    image = forms.ImageField(label='Bukti Pembayaran', help_text='Upload Bukti Transfer', required=True)
    class Meta:
        model = Administrasi
        fields = ['image',]

class AdministrasiTransferForm(forms.ModelForm):
    image = forms.ImageField(label='Bukti Pembayaran', help_text='Upload Bukti Transfer', required=True)
    class Meta:
        model = Administrasi
        fields = ['image',]

class SliderForm(forms.ModelForm):
    image = forms.ImageField(label='Foto Slide', required=True)
    caption = forms.CharField(label='Caption', max_length=50, required=True)
    class Meta:
        model = Slider
        fields = ['image', 'caption',]
    def clean_image(self):
        image = self.cleaned_data['image']
        if image:
            from django.core.files.images import get_image_dimensions
            w, h = get_image_dimensions(image)

            if w > 958 or h > 460:
                raise forms.ValidationError(
                u'That image is un suitable. The image needs to be width : 958px height :460px ')
        return image

class AbsensiForm(forms.ModelForm):
    is_present = forms.ModelMultipleChoiceField(
        label='Daftar Kehadiran',
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    tutor_pendamping = forms.ModelMultipleChoiceField(
        label='Asisten Tutor',
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = PracticeAttendance
        fields = ('is_present', 'tutor_pendamping',)

class DeskripsiAVCForm(forms.ModelForm):
    # value = forms.CharField(
    #     label='Isi Deskripsi',
    #     widget=forms.Textarea)
    class Meta:
        model = SettingsVariable
        fields = ['value']
