#user_form = UserForm(data = request.POST)
#user = user_form.save(commit = False)
# if user_form.cleaned_data['password1'] != user_form.cleaned_data['password2']:
#     user_form.add_error('password1', u"Password tidak sama")
#     context={'regis_form' : regis_form, 'user_form' : user_form, 'profile_form' : profile_form,
#     'administrasi_form' : administrasi_form,
#     'registered' : registered}
#     condition_query = Article.objects.get(title="Syarat dan Ketentuan")
#     context['conditions'] = condition_query
#     return render (request, 'public/register.html', context)
# user.set_password(user.password)
# regis = regis_form.save(commit = False)
# user.first_name= regis.first_name
# user.last_name = regis.last_name

username = user_form.cleaned_data.get('username')
raw_password = user_form.cleaned_data.get('password1')
user = authenticate(username=username, password=raw_password)
login(request, user)


            #email
            subject = 'terima kasih telah mendaftar'
            message = 'Selamat datang, segera lunasi pembayaran anda '
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently = True)
            kelas= Kelas.objects.get(nama_kelas='Basic')
            profile = profile_form.save(commit = False)
            profile.user_kelas = kelas
            today = timezone.now().date()
            # logkelas = LogKelas.objects.create(kelas_current=kelas.nama_kelas, user=user.username,
            #     joined_date= today)
            # user.save()
            profile.user = user
            if 'photo' in request.FILES :
                profile.photo = request.FILES['photo']
            registered = True
            administrasi = administrasi_form.save(commit = False)
            regis_pay = AdministrationType.objects.get(paymentstype="Registration and First Dues")
            administrasi.jenis = regis_pay
            administrasi.user = user
            profile.save()
            administrasi.save()

        else:
            print (
             profile_form.errors, regis_form.errors)


{% for field in user_form %}
<p>
{{ field.label_tag }}<br>
{{ field }}
{% if field.help_text %}
<small style="color: grey">{{ field.help_text }}</small>
{% endif %}
{% for error in field.errors %}
<p style="color: red">{{ error }}</p>
{% endfor %}
</p>
{% endfor %}
{% bootstrap_form regis_form %}
{% bootstrap_form profile_form%}
{% bootstrap_form administrasi_form %}



from django.core.mail import EmailMultiAlternatives

subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
text_content = 'This is an important message.'
html_content = '<p>This is an <strong>important</strong> message.</p>'
msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
msg.attach_alternative(html_content, "text/html")
msg.send()
/**forms.py*/




event_name = forms.CharField(label='Nama Acara',max_length=50)
corporate = forms.CharField(label='Instansi', max_length=50)
desc = forms.CharField(label='Deskripsi Singkat')
sender = forms.CharField(label='Pengaju',max_length=20)
phone = forms.CharField(label='Nomor Handphone',max_length=20)
email = forms.EmailField(label='E-mail Pengaju',)
image = forms.ImageField(label='Pamflet atau Poster', required=False,)
attachment = forms.FileField(label='File Pendukung', help_text='*harus .pdf', required=False)
event_date = forms.DateField(label='Tanggal Acara', verbose_name="Pengajuan Kerja Sama")
class Meta:
    model = Event
    fields = ['event_name', 'corporate', 'desc', 'sender', 'phone','email',
    'image', 'attachment', 'event_date']
    widget = {
         'desc': Textarea(attrs={'cols': 80, 'rows': 20}),
    }
