from django.forms import ModelForm
from .models import Event

#create the form class
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'corporate', 'desc', 'sender', 'phone','email',
        'image', 'attachment', 'event_date']
