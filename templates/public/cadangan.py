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
