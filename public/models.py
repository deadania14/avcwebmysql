from django.db import models
from django.utils import timezone

class Event(models.Model):
    event_id = models.AutoField(primary_key = True)
    event_name = models.CharField(max_length=20)
    corporate = models.CharField(max_length=50)
    desc = models.TextField()
    sender = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    attachment = models.FileField(blank=True)
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
