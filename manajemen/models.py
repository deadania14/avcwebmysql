from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Article(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='images/articles')
    created_date = models.DateTimeField(
        default = timezone.now
    )
    updated_date = models.DateTimeField(
        blank = True, null = True
    )
    published_date = models.DateTimeField(
        blank = True, null = True
    )
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def update(self):
        self.update_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title

class Practice(models.Model):
    date = models.DateTimeField(blank = False)
    place = models.CharField(max_length= 50)
    note = models.TextField()
    created_date = models.DateTimeField(
        default = timezone.now
        )
    def __str__(self):
        return "{}".format(self.date.date())

class Kelas(models.Model):
    nama_kelas = models.CharField(default='', max_length=50)
    user = models.ManyToManyField(User, related_name="kelas")
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

    def schedule_last_three_months(self):
        today = timezone.now()
        three_months_ago = today + timezone.timedelta(days=-130)
        schedule_class = PracticeAttendance.objects.filter(kelas=self)
        schedule_class_three_months_ago = schedule_class.filter(
            practice__date__gte=three_months_ago,
            practice__date__lte=today
        )
        return schedule_class_three_months_ago.count()


class PracticeAttendance(models.Model):
    kelas = models.ForeignKey(Kelas, related_name="practice_attendances", null=True)
    practice = models.ForeignKey(Practice, related_name= "practice_attendances")
    is_present = models.ManyToManyField(User, related_name= "practice_attendances", blank=True)
    tutor = models.ForeignKey(User, related_name= "tutor_practice_attendances", null=True)
    tutor_pendamping = models.ManyToManyField(User, related_name= "tutor_pendamping_practice_attendances", blank=True)
    updated_date = models.DateField(
        blank = True, null = True
    )
    def update(self):
        self.updated_date = timezone.now()
        self.save()


class AdministrationType(models.Model):
    paymentstype = models.CharField(max_length = 50 )
    nominal = models.IntegerField()
    created_date = models.DateTimeField(
        default = timezone.now
    )
    def __str__(self):
        return self.paymentstype

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
    method = models.CharField(max_length=20, choices = method_choices, default= 'cash')
    image = models.ImageField(null=True, blank=True, upload_to='images/bukti_payments')
    status = models.CharField(max_length=20, choices = status_choices, default= 'pending')
    created_date = models.DateTimeField(
        default = timezone.now
    )
    class Meta:
        ordering =['-created_date',]

    def __str__(self):
        return self.jenis.paymentstype
