from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from manajemen.models import Article, Administrasi, AdministrationType
from .models import Event
from .forms import EventForm, UserForm, UserProfileForm, AdministrasiForm

def index(request):
    context={}
    events_query = Event.objects.all()[:4]
    context['events'] = events_query
    articles_query = Article.objects.all()
    context['articles'] = articles_query
    return render(request, 'public/index.html', context)

def about(request):
    context={}
    sejarah = Article.objects.get(title = 'Sejarah AVC')
    context['history'] = sejarah
    companyprofile = Article.objects.get(title = 'Company Profile')
    context['cprofile'] = companyprofile
    return render(request, 'public/about.html', context)

def contact(request):
    context={}
    contact_us = Article.objects.get(title = 'Hubungi Kami')
    context['contactus'] = contact_us
    return render(request, 'public/contact_us.html', context)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)
        administrasi_form = AdministrasiForm(data = request.POST)
        if user_form.is_valid() and profile_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            #email
            subject = 'terima kasih telah mendaftar'
            message = 'Selamat datang, segera lunasi pembayaran anda '
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently = True)

            profile = profile_form.save(commit = False)
            profile.user = user
            if 'photo' in request.FILES :
                profile.photo = request.FILES['photo']
            profile.save()
            registered = True
            administrasi = administrasi_form.save(commit = False)
            regis_pay = AdministrationType.objects.get(paymentstype="Registration and First Dues")
            administrasi.jenis = regis_pay
            administrasi.user = user
            administrasi.save()

        else:
            print (user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        administrasi_form = AdministrasiForm()
    return render (request, 'public/register.html',
                    {'user_form' : user_form, 'profile_form' : profile_form,
                    'administrasi_form' : administrasi_form,
                    'registered' : registered})

def event_detail(request, event_id):
    context={}
    eventid_query= Event.objects.get(id=event_id)
    context['eventid'] = eventid_query
    return render(request, 'public/event_detail.html', context)

#def registration(request):
#    context={}
#    return render(request, 'public/registration.html', context)

def event_new(request):
    context={}
    deal_event= Event.objects.all()
    context["devent"] = deal_event
    if request.method=="POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            nevent = form.save(commit = False)
            nevent.status_choices = "waiting"
            nevent.created_date= timezone.now()
            nevent.save()
            #email
            subject = 'Acara'+nevent.event_name+'Akan Dipertimbangkan'
            message = 'Terima kasih telah mengirim ajuan. Acara Anda akan kami pertimbangkan segera.'
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently = True)

            return HttpResponseRedirect(reverse('public:event_detail', args=(nevent.id,)))
    else :
        form = EventForm()
    return render(request, 'public/event_new.html', {'form':form}, context)
