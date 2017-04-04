from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from manajemen.models import Article
from .models import Event
from .forms import EventForm, UserForm, UserProfileForm

def index(request):
    context={}
    events_query = Event.objects.all()
    context['events'] = events_query
    articles_query = Article.objects.all()
    context['articles'] = articles_query
    return render(request, 'public/index.html', context)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            if 'photo' in request.FILES :
                profile.photo = request.FILES['photo']
            profile.save()
            registered = True
        else:
            print (user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render (request, 'public/register.html',
                    {'user_form' : user_form, 'profile_form' : profile_form,
                    'registered' : registered})

def event_detail(request, event_id):
    context={}
    eventid_query= Event.objects.get(id=event_id)
    context['eventid'] = eventid_query
    return render(request, 'public/event_detail.html', context)

def registration(request):
    context={}
    return render(request, 'public/registration.html', context)

def event_new(request):
    if request.method=="POST":
        form = EventForm(request.POST)
        if form.is_valid():
            nevent = form.save(commit = False)
            nevent.status_choices = "waiting"
            nevent.created_date= timezone.now()
            nevent.save()
            return HttpResponseRedirect(reverse('public:event_detail', args=(nevent.id,)))
    else :
        form = EventForm()
    return render(request, 'public/event_new.html', {'form':form})
