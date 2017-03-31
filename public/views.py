from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Event
from .forms import EventForm
from manajemen.models import Article

def index(request):
    context={}
    events_query = Event.objects.all()
    context['events'] = events_query
    articles_query = Article.objects.all()
    context['articles'] = articles_query
    return render(request, 'public/index.html', context)

def event_detail(request, event_id):
    context={}
    eventid_query= Event.objects.get(id=event_id)
    context['eventid'] = eventid_query
    return render(request, 'public/event_detail.html', context)

def registration(request):
    context={}
    return render(request, 'public/registration.html', context)
