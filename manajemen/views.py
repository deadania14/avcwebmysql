from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, Practice, Administrasi, Kelas, PracticeAttendance, Inventory
from .forms import ArticleForm, MainArticleForm, SchedulesForm, ClassForm, AbsensiForm, AbsensiNewForm, AVCContactForm, NewEventForm, EditBarangForm
from public.models import UserProfile, Event, SettingsVariable

from rolepermissions.decorators import has_role_decorator

@login_required
@has_role_decorator('manajemen')
def index(request):
    if request.user.profile.tipe_user == 'member':
        return HttpResponseRedirect(reverse('member:index'))
    context={}
    return render(request, 'manajemen/index.html', context)

def list_article(request):
    context={}
    articles_query = Article.objects.all()
    context['articles'] = articles_query
    return render(request, 'manajemen/list_article.html', context)

@has_role_decorator('hpd')
def home_hpd(request):
    context={}
    articles_query = Article.objects.all()
    context['articles'] = articles_query
    return render(request, 'manajemen/hpd.html', context)

@has_role_decorator('psdm')
def home_psdm(request):
    context={}
    today = timezone.now().date()
    user_profile = UserProfile.objects.all()
    context['userprofiles']= user_profile
    practice_query = Practice.objects.all()
    context['practices'] = practice_query
    kelas_query = Kelas.objects.all()
    context['classes'] = kelas_query
    present_query = PracticeAttendance.objects.all()
    context['presents'] = present_query
    context['now'] = today
    return render(request, 'manajemen/psdm.html', context)

@has_role_decorator('tutor')
def home_tutor(request):
    context={}
    today = timezone.now().date()
    practice_query = Practice.objects.filter(date__gte=today)
    context['practices'] = practice_query
    present_query = PracticeAttendance.objects.filter(practice__date__gte=today)
    context['presents'] = present_query
    context['now'] = timezone.now().date()
    return render(request, 'manajemen/tutor.html', context)

@has_role_decorator('bendahara')
def home_keuangan(request):
    context={}
    administrasi_query = Administrasi.objects.all()
    context['adminitrasis']= administrasi_query
    context['saldo'] = Administrasi.saldo.get_saldo()
    return render(request, 'manajemen/keuangan.html', context)

@has_role_decorator('inventaris')
def home_inventaris(request):
    context={}
    inventory_query = Inventory.objects.all()
    context['inventories']= inventory_query
    return render(request, 'manajemen/inventaris.html', context)

@has_role_decorator('program')
def home_acara(request):
    context={}
    acara_query = Event.objects.all()
    context['acaras']= acara_query
    return render(request, 'manajemen/acara.html', context)

def confirmation_event(request, event_id):
    eventconf = Event.objects.get(id=event_id)
    eventconf.status = "deal"
    eventconf.save()
    return HttpResponseRedirect(reverse('manajemen:home_acara'))

def cancel_event(request, event_id):
    eventconf = Event.objects.get(id=event_id)
    eventconf.status = "cancelled"
    eventconf.save()
    return HttpResponseRedirect(reverse('manajemen:home_acara'))


def confirmation_payment(request, payment_id):
    payment = Administrasi.objects.get(id=payment_id)
    payment.status = "paid"
    payment.save()
    if payment.jenis.paymentstype == 'Registration and First Dues':
        userp = UserProfile.objects.get(user = payment.user)
        userp.is_registration_paid = True
        userp.save()
    return HttpResponseRedirect(reverse('manajemen:home_keuangan'))

def cancel_payment(request, payment_id):
    payment = Administrasi.objects.get(id=payment_id)
    payment.status = "cancelled"
    payment.save()
    if payment.jenis.paymentstype == 'Registration and First Dues':
        payment.user.is_active = False
        payment.user.save()
    return HttpResponseRedirect(reverse('manajemen:home_keuangan'))

def detail_article(request, article_id):
    context={}
    articleid_query= get_object_or_404(Article, id=article_id)
    context['articleid'] = articleid_query
    return render(request, 'manajemen/detail_article.html', context)

def detail_schedule(request, schedule_id):
    context={}
    schedule_query= Practice.objects.get(id=schedule_id)
    context['scheduleid'] = schedule_query
    return render(request, 'manajemen/detail_schedule.html', context)

def delete_schedule(request, schedule_id):
    practice_query = Practice.objects.get(id=schedule_id)
    practice_query.delete()
    return HttpResponseRedirect(reverse('manajemen:home_psdm'))

def edit_barang(request, barang_id):
    context={}
    barang = get_object_or_404(Inventory, id=barang_id)
    if request.method=="POST":
        form_edit_barang = EditBarangForm(request.POST, instance = barang)
        if form_edit_barang.is_valid():
            barang = form_edit_barang.save(commit = False)
            barang.updated_date= timezone.now()
            barang.save()
            return HttpResponseRedirect(reverse('manajemen:home_inventaris', ))
    else :
        form_edit_barang = EditBarangForm(instance = barang)
    return render(request, 'manajemen/edit_barang.html', {'form_edit_barang':form_edit_barang})

def edit_contact(request):
    address = SettingsVariable.objects.get(key="address")
    phone1  = SettingsVariable.objects.get(key="phone1")
    phone2  = SettingsVariable.objects.get(key="phone2")
    email  = SettingsVariable.objects.get(key="email")
    facebook  = SettingsVariable.objects.get(key="facebook")
    instagram  = SettingsVariable.objects.get(key="instagram")
    twitter  = SettingsVariable.objects.get(key="twitter")
    youtube  = SettingsVariable.objects.get(key="youtube")
    default_data = {'address':address.value, 'phone1': phone1.value,
    'phone2':phone2.value, 'email':email.value, 'facebook':facebook.value,
    'instagram':instagram.value, 'twitter':twitter.value, "youtube":youtube.value,}

    if request.method=="POST":
        form_edit_contact = AVCContactForm(request.POST)
        if form_edit_contact.is_valid():
            address.value = form_edit_contact.cleaned_data.get('address')
            address.save()
            phone1.value = form_edit_contact.cleaned_data.get('phone1')
            phone1.save()
            phone2.value = form_edit_contact.cleaned_data.get('phone2')
            phone2.save()
            email.value = form_edit_contact.cleaned_data.get('email')
            email.save()
            facebook.value = form_edit_contact.cleaned_data.get('facebook')
            facebook.save()
            twitter.value = form_edit_contact.cleaned_data.get('twitter')
            twitter.save()
            instagram.value = form_edit_contact.cleaned_data.get('instagram')
            instagram.save()
            youtube.value = form_edit_contact.cleaned_data.get('youtube')
            youtube.save()
            return HttpResponseRedirect(reverse('manajemen:home_hpd'))
    else :
        form_edit_contact = AVCContactForm(initial = default_data)
    return render(request, 'manajemen/edit_contact.html', {'form_edit_contact':form_edit_contact})

def edit_article(request, article_id):
    narticle = get_object_or_404(Article, id=article_id)
    if request.method=="POST":
        form_edit_article = ArticleForm(request.POST, instance = narticle)
        if form_edit_article.is_valid():
            narticle = form_edit_article.save(commit = False)
            narticle.author = request.user
            narticle.updated_date= timezone.now()
            narticle.save()
            return HttpResponseRedirect(reverse('manajemen:detail_article', args=(narticle.id,)))
    else :
        form_edit_article = ArticleForm(instance = narticle)
    return render(request, 'manajemen/edit_article.html', {'form_edit_article':form_edit_article})

def edit_mainarticle(request, article_id):
    narticle = get_object_or_404(Article, id=article_id)
    if request.method=="POST":
        form_edit_article = MainArticleForm(request.POST, instance = narticle)
        if form_edit_article.is_valid():
            narticle = form_edit_article.save(commit = False)
            narticle.author = request.user
            narticle.updated_date= timezone.now()
            narticle.save()
            return HttpResponseRedirect(reverse('manajemen:detail_article', args=(narticle.id,)))
    else :
        form_edit_article = MainArticleForm(instance = narticle)
    return render(request, 'manajemen/edit_article.html', {'form_edit_article':form_edit_article})

def edit_schedule(request, schedule_id):
    nschedule = get_object_or_404(Practice, id=schedule_id)
    if request.method=="POST":
        form_edit_schedule = SchedulesForm(request.POST, instance = nschedule)
        if form_edit_schedule.is_valid():
            nschedule = form_edit_schedule.save(commit = False)
            nschedule.created_date= timezone.now()
            nschedule.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form_edit_schedule = SchedulesForm(instance = nschedule)
    return render(request, 'manajemen/edit_schedule.html', {'form_edit_schedule':form_edit_schedule})

def edit_kelas(request, kelas_id):
    nclass = get_object_or_404(Kelas, id=kelas_id)
    if request.method=="POST":
        form_edit_kelas = ClassForm(request.POST, instance = nclass)
        if form_edit_kelas.is_valid():
            nclass.updated_date= timezone.now()
            nclass.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm',))
    else :
        form_edit_kelas = ClassForm(instance = nclass)
    return render(request, 'manajemen/edit_class.html', {'form_edit_kelas':form_edit_kelas})

def edit_attendance(request, attendance_id):
    npresent = get_object_or_404(PracticeAttendance, id=attendance_id)
    if request.method=="POST":
        form_edit_absensi = AbsensiForm(request.POST, instance = npresent)

        if form_edit_absensi.is_valid():
            form_edit_absensi.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form_edit_absensi = AbsensiForm(instance = npresent)
    form_edit_absensi.fields['is_present'].queryset = User.objects.filter(kelas=npresent.kelas)
    form_edit_absensi.fields['tutor_pendamping'].queryset = User.objects.filter(profile__tipe_user='tutor').exclude(id=npresent.tutor.id)
    return render(request, 'manajemen/edit_attendance.html', {'form_edit_absensi':form_edit_absensi})

def new_event(request):
    context={}
    deal_event= Event.objects.all()
    context["devent"] = deal_event
    if request.method=="POST":
        form_new_event = NewEventForm(request.POST, request.FILES)
        if form_new_event.is_valid():
            nevent = form_new_event.save(commit = False)
            nevent.corporate = "AVC"
            nevent.sender = request.user
            nevent.status_choices = "deal"
            nevent.created_date= timezone.now()
            nevent.save()
            return HttpResponseRedirect(reverse('manajemen:home_acara', ))
    else :
        form_new_event = NewEventForm()
    return render(request, 'manajemen/new_event.html', {'form_new_event':form_new_event}, context)

def new_attendance(request):
    if request.method=="POST":
        form_new_absensi = AbsensiNewForm(request.POST)
        if form_new_absensi.is_valid():
            npresent = form_new_absensi.save(commit = False)
            npresent.updated_date= timezone.now()
            npresent.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form_new_absensi = AbsensiNewForm()
    form_new_absensi.fields['tutor'].queryset = User.objects.filter(profile__tipe_user='tutor')
    form_new_absensi.fields['practice'].queryset = Practice.objects.filter(date__gte=timezone.now().date())
    return render(request, 'manajemen/new_attendance.html', {'form_new_absensi':form_new_absensi})

def new_article(request):
    if request.method=="POST":
        form_edit_article = ArticleForm(request.POST)
        if form_edit_article.is_valid():
            narticle = form_edit_article.save(commit = False)
            narticle.author = request.user
            narticle.published_date= timezone.now()
            narticle.save()
            return HttpResponseRedirect(reverse('manajemen:detail_article', args=(narticle.id,)))
    else :
        form_edit_article = ArticleForm()
    return render(request, 'manajemen/new_article.html', {'form_edit_article':form_edit_article})

def new_schedule(request):
    if request.method=="POST":
        form_edit_schedule = SchedulesForm(request.POST)
        print(form_edit_schedule)
        if form_edit_schedule.is_valid():
            nschedule = form_edit_schedule.save(commit = False)
            nschedule.created_date= timezone.now()
            nschedule.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form_edit_schedule = SchedulesForm()
    return render(request, 'manajemen/edit_schedule.html', {'form_edit_schedule':form_edit_schedule})

def new_kelas(request):
    if request.method=="POST":
        form_new_kelas = ClassForm(request.POST)
        if form_new_kelas.is_valid():
            nclass = form_new_kelas.save(commit = False)
            nclass.updated_date= timezone.now()
            nclass.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form_new_kelas = ClassForm()
    form_new_kelas.fields['user'].queryset = User.objects.filter(profile__is_have_kelas=False)
    return render(request, 'manajemen/new_class.html', {'form_new_kelas':form_new_kelas})
