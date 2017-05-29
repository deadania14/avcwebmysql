from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Article(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='images/articles')
    is_mainarticle = models.BooleanField(default = False)
    is_concertarticle = models.BooleanField(default= False)
    is_publish = models.BooleanField(default= False)
    created_date = models.DateTimeField(
        default = timezone.now
    )
    updated_date = models.DateTimeField(
        blank = True, null = True
    )
    published_date = models.DateTimeField(
        blank = True, null = True
    )
    class Meta:
        ordering =['-updated_date',]
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def update(self):
        self.updated_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title

class Practice(models.Model):
    date = models.DateTimeField(blank = False)
    place = models.CharField(max_length= 100)
    note = models.TextField()
    created_date = models.DateTimeField(
        default = timezone.now
        )
    class Meta:
        ordering =['-date',]
    def __str__(self):
        return "{} {}".format(self.date.date(),self.date.time() )

class Kelas(models.Model):
    nama_kelas = models.CharField(default='', max_length=50)
    note = models.TextField(null= True)
    updated_date = models.DateField(
        blank = True, null = True
    )
    def update(self):
        self.updated_date = timezone.now()
        self.save()

    class Meta:
        ordering =['-updated_date',]
    def __str__(self):
        return self.nama_kelas

class LogKelas(models.Model):
    kelas_current = models.ForeignKey(Kelas, related_name= 'log_kelas_current')
    user = models.ForeignKey(User, related_name='log_kelas_user')
    kelas_before = models.ForeignKey(Kelas, related_name='log_kelas_before', null=True)
    joined_date = models.DateTimeField(
        default = timezone.now
        )
    class Meta:
        ordering =['-joined_date',]

class PracticeAttendance(models.Model):
    kelas = models.ForeignKey(Kelas, related_name="practice_attendances", null=True)
    practice = models.ForeignKey(Practice, related_name= "practice_attendances")
    daftar_orang = models.ManyToManyField(User, related_name= "user_practice_attendances", blank=True)
    is_present = models.ManyToManyField(User, related_name= "practice_attendances", blank=True)
    tutor = models.ForeignKey(User, related_name= "tutor_practice_attendances", null=True)
    tutor_pendamping = models.ManyToManyField(User, related_name= "tutor_pendamping_practice_attendances", blank=True)
    updated_date = models.DateField(
        blank = True, null = True
    )
    def update(self):
        self.updated_date = timezone.now()
        self.save()
    class Meta:
        ordering =['-updated_date',]


class AdministrationType(models.Model):
    paymentstype = models.CharField(max_length = 50 )
    nominal = models.PositiveIntegerField()
    created_date = models.DateTimeField(
        default = timezone.now
    )
    updated_date = models.DateField(
    blank = True, null = True
    )
    def __str__(self):
        return self.paymentstype
    def update(self):
        self.updated_date = timezone.now()
        self.save()

class AdministrasiManager(models.Manager):
    def get_saldo(self):
        saldo = self.filter(status='paid').aggregate(Sum('nominal'))
        return saldo['nominal__sum']

class Administrasi(models.Model):
    method_choices= (
        ('cash','Cash',),
        ('transfer', 'Transfer',),
    )
    status_choices= (
        ('pending','Pending',),
        ('paid', 'Paid',),
        ('cancelled', 'Cancelled',),
    )
    user = models.ForeignKey(User, related_name="administrasi", null = True)
    jenis = models.ForeignKey(AdministrationType,related_name= "administrasi_jenis", null = True)
    nominal = models.PositiveIntegerField(null=True, blank=True)
    method = models.CharField(max_length=20, choices = method_choices, default= 'cash')
    image = models.ImageField(null=True, upload_to='images/bukti_payments', blank=True)
    status = models.CharField(max_length=20, choices = status_choices, default= 'pending')
    note = models.TextField(blank = True)
    created_date = models.DateTimeField(
        default = timezone.now
    )

    saldo = AdministrasiManager()
    objects = models.Manager() # The default manager.
    class Meta:
        ordering =['-created_date',]

    def __str__(self):
        return self.jenis.paymentstype

class Inventory(models.Model):
    thingsname = models.CharField(max_length=40)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    detail = models.CharField(max_length=100)
    note = models.CharField(max_length=200)
    created_date = models.DateTimeField(
        default = timezone.now
    )
    updated_date = models.DateTimeField(
        blank = True, null = True
    )
    def update(self):
        self.updated_date = timezone.now()
        self.save()

class Meeting(models.Model):
    title = models.CharField(max_length=40)
    place = models.CharField(max_length=100, null=True, blank=True)
    date_meet = models.DateField(blank=True, null=True)
    user = models.ManyToManyField(User, related_name= "user_meeting_attendances", blank=True)
    note = models.TextField()
    created_date = models.DateField(
        default = timezone.now
    )
    updated_date = models.DateField(
        default = timezone.now
    )
