from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from manajemen.models import PracticeAttendance, Kelas

class Event(models.Model):
    event_name = models.CharField(max_length=50)
    corporate = models.CharField(max_length=50)
    desc = models.TextField()
    sender = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(null=True, blank=True, upload_to='images/events')
    attachment = models.FileField(blank=True, verbose_name = "proposal atau undangan", upload_to='files/events')
    event_date = models.DateTimeField( default = timezone.now)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    status_choices= (
        ('waiting','Waiting',),
        ('deal', 'Deal',),
        ('cancelled', 'Cancelled',),
        ('done', 'Done',),
    )
    event_status = models.CharField(max_length=20, default = "waiting", choices= status_choices)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.event_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name= "profile")
    gender_choices = (
        ('wanita', 'Wanita',),
        ('pria', 'Pria',),
    )
    tipe_user_choices = (
        ('member', 'Member',),
        ('tutor', 'Tutor',),
        ('ketua/wakil', 'Ketua/Wakil',),
        ('sekretaris', 'Sekretaris',),
        ('bendahara', 'Bendahara',),
        ('hpd', 'HPD'),
        ('psdm', 'PSDM'),
        ('inventaris', 'Inventaris',),
        ('program','Program',),
    )
    tipe_user = models.CharField(max_length = 20, default = "member", choices=tipe_user_choices)
    gender = models.CharField(max_length = 10, default = "pria", choices= gender_choices)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    photo = models.ImageField(null=True, blank=True, upload_to='images/profile_images')
    update_time = models.DateTimeField(
        default=timezone.now)
    is_registration_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def schedule_last_three_months(self):
        self_class = Kelas.objects.get(user=self.user)
        schedule_last_three_months = self_class.schedule_last_three_months()
        return schedule_last_three_months

    def attend_last_three_months(self):
        today = timezone.now()
        three_months_ago = today + timezone.timedelta(days=-130)
        attend_class = PracticeAttendance.objects.filter(is_present=self.user)
        attend_class_three_months_ago = attend_class.filter(
            practice__date__gte=three_months_ago,
            practice__date__lte=today
        )
        return attend_class_three_months_ago.count()

    def attend_last_three_months_percent(self):
        attend_last_three_months =  self.attend_last_three_months()
        self_class = Kelas.objects.get(user=self.user)
        schedule_last_three_months = self_class.schedule_last_three_months()
        if schedule_last_three_months == 0:
            return 0.0
        return attend_last_three_months/schedule_last_three_months * 100

class SettingsVariable (models.Model):
    key = models.CharField(max_length=255, null=True)
    value = models.TextField(null=True, blank = True)
    updated_date = models.DateTimeField(
        blank = True, null = True
    )
    def update(self):
        self.updated_date = timezone.now()
        self.save()
