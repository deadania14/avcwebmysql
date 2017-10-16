from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from manajemen.models import PracticeAttendance, Kelas
from .validators import validate_file_extension

class Slider(models.Model):
    image = models.ImageField(null= True, blank= True, upload_to='images/slider')
    caption = models.CharField(max_length= 50)
    publisher = models.CharField(max_length= 40)
    updated_date = models.DateTimeField(
        blank = True, null = True
    )
    class Meta:
        ordering =['-updated_date',]
    def update(self):
        self.updated_date = timezone.now()
        self.save()

class Event(models.Model):
    event_name = models.CharField(max_length=50)
    corporate = models.CharField(max_length=50)
    desc = models.TextField()
    sender = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/events')
    attachment = models.FileField(verbose_name = "proposal atau undangan", upload_to='files/events', validators=[validate_file_extension], blank=True)
    event_date = models.DateField( default = timezone.now)
    is_publish = models.BooleanField(default= False)
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
    class Meta:
        ordering =['-event_date',]

BATAS_KELUAR = 60
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name= "profile", on_delete=models.CASCADE)
    user_kelas = models.ForeignKey(Kelas, related_name="profiles", null=True, blank=True)
    gender_choices = (
        ('wanita', 'Wanita',),
        ('pria', 'Pria',),
    )
    tipe_user_choices = (
        ('member', 'Member',),
        ('tutor', 'Tutor',),
    )
    tipe_user = models.CharField(max_length = 20, default = "member", choices=tipe_user_choices)
    gender = models.CharField(max_length = 10, default = "pria", choices= gender_choices)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    about = models.TextField(null=True, blank=True)
    plbirth = models.CharField(max_length=40, null=True, blank = True)
    date_birth = models.DateField(blank = True, null= True)
    photo = models.ImageField(null=True, blank=True, upload_to='images/profile_images')
    update_time = models.DateTimeField(
        default=timezone.now)
    is_registration_paid = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

    def schedule_last_three_months(self):
        today = timezone.now()
        three_months_ago = today + timezone.timedelta(days=-BATAS_KELUAR)
        attend_class = PracticeAttendance.objects.filter(daftar_orang=self.user)
        attend_class_three_months_ago = attend_class.filter(
            practice__date__gte=three_months_ago,
            practice__date__lte=today
        )
        return attend_class_three_months_ago.count()

    def attend_last_three_months(self):
        today = timezone.now()
        three_months_ago = today + timezone.timedelta(days=-BATAS_KELUAR)
        attend_class = PracticeAttendance.objects.filter(is_present=self.user)
        attend_class_three_months_ago = attend_class.filter(
            practice__date__gte=three_months_ago,
            practice__date__lte=today
        )
        return attend_class_three_months_ago.count()

    def attend_last_three_months_percent(self):
        attend_last_three_months =  self.attend_last_three_months()
        schedule_last_three_months = self.schedule_last_three_months()
        if schedule_last_three_months != 0:
            return attend_last_three_months/schedule_last_three_months * 100
        else:
            return 0.0

    def user_check_schedule(self):
        check_schedule = PracticeAttendance.objects.filter(daftar_orang=self.user)
        return check_schedule.count()

    def new_member(self):
        if self.user.is_active and self.user_check_schedule() == 0:
            return True
        else:
            return False

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

class Timeline(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, related_name="sender_broadcast", null=True,)
    message = models.CharField(max_length=255)
    created_date = models.DateTimeField(
            default=timezone.now)
    class Meta:
        ordering =['-created_date',]

class SettingsVariable (models.Model):
    key = models.CharField(max_length=255, null=True)
    value = models.TextField(null=True, blank = True)
    updated_date = models.DateTimeField(
        blank = True, null = True
    )
    def update(self):
        self.updated_date = timezone.now()
        self.save()

class QuenstionAnswer(models.Model):
    question = models.CharField(max_length=255, null=True)
    answer = models.TextField(null=True)
    created_date= models.DateTimeField(
        blank = True, null = True
    )
    updated_date = models.DateTimeField(
        blank = True, null = True
    )
    def created_date(self):
        self.updated_date = timezone.now()
        self.save()
