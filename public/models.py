from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
        ('lainnya', 'Lainnya',),
    )
    gender = models.CharField(max_length = 10, default = "pria", choices= gender_choices)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    photo = models.ImageField(null=True, blank=True, upload_to='images/profile_images')
    update_time = models.DateTimeField(
            default=timezone.now)
    def __str__(self):
        return self.user.username
