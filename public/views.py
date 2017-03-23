from django.shortcuts import render
from .models import Event

def index(request):
    context={}
    events_query = Event.objects.all()
    context['events'] = events_query
    return render(request, 'public/index.html', context)
