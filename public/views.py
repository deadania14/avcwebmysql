from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
##
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
##
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from .forms import SignUpForm, RegisterTransferForm, NewPaymentOfferForm, SliderForm
from manajemen.models import Article, Administrasi, AdministrationType, PracticeAttendance, Kelas
from public.models import SettingsVariable
from .models import Event, Slider, UserProfile, Kelas, Timeline
from .forms import EventForm, UserProfileEditForm, AdministrasiForm, UserRegister
from manajemen.models import Practice, Kelas, PracticeAttendance, LogKelas

from rolepermissions.decorators import has_role_decorator

def index(request):
    if request.method=="POST":
        slider_form = SliderForm(request.POST, request.FILES)
        if slider_form.is_valid():
            nslide = slider_form.save(commit=False)
            nslide.updated_date = timezone.now()
            nslide.publisher = request.user
            nslide.save()
        else:
            print (slider_form.errors)
    else:
        slider_form = SliderForm()
    context={'slider_form' : slider_form,}
    articles_query = Article.objects.filter(is_mainarticle=False).filter(is_publish=True)[:4]
    context['articles'] = articles_query
    slider_query = Slider.objects.all()[:4]
    context['sliders'] = slider_query
    return render(request, 'public/index.html', context)

def about(request):
    context={}
    sejarah = Article.objects.get(title = 'Sejarah AVC')
    context['history'] = sejarah
    companyprofile = Article.objects.get(title = 'Company Profile')
    context['cprofile'] = companyprofile
    return render(request, 'public/about.html', context)

def konser(request):
    context={}
    konser = Article.objects.filter(is_concertarticle= True)
    context['concerts'] = konser
    return render(request, 'public/konser.html', context)

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('public:myprofile',))
    registered = False
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        regisadm_form = AdministrasiForm(request.POST)
        if user_form.is_valid() and regisadm_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            regadm = regisadm_form.save(commit=False)
            regis_pay = AdministrationType.objects.get(paymentstype="Registration and First Dues")
            regadm.jenis = regis_pay
            regadm.user = user
            regadm.save()
            kelas = Kelas.objects.get(nama_kelas='Basic')
            today = timezone.now().date()
            LogKelas.objects.create(kelas_current=kelas, user=user,
            joined_date= today)
            #<EMAIL>
            subject = 'Selamat Datang ' + str(user)
            message = 'Terima kasih telah mendaftar. Selamat datang, segera lunasi pembayaran Anda'
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently = True)
            bendaharas = User.objects.filter(groups__name='bendahara')
            subjectb = 'Pendaftar Baru '+ str(user)
            messageb = 'Pendaftar dengan nama '+user.first_name+ ' memilih pembayaran secara '+ str(regadm.method) +'.'
            from_emailb = settings.EMAIL_HOST_USER
            to_list = [settings.EMAIL_HOST_USER]
            for bendahara in bendaharas:
                to_list.append(bendahara.email)
            send_mail(subjectb, messageb, from_emailb, to_list, fail_silently = True)
            # </EMAIL>
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('public:myprofile')
    else:
        user_form = SignUpForm()
        regisadm_form = AdministrasiForm()
    context={'user_form' : user_form, 'regisadm_form': regisadm_form,}
    condition_query = Article.objects.get(title="Syarat dan Ketentuan")
    context['conditions'] = condition_query
    return render (request, 'public/register.html', context)

def event_detail(request, event_id):
    context={}
    eventid_query= Event.objects.get(id=event_id)
    context['eventid'] = eventid_query
    return render(request, 'public/event_detail.html', context)

def article_detail(request, article_id):
    context={}
    articleid_query= Article.objects.get(id=article_id)
    context['articleid'] = articleid_query
    return render(request, 'public/article_detail.html', context)

def events(request):
    if request.method=="POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            nevent = form.save(commit = False)
            nevent.status_choices = "waiting"
            nevent.created_date= timezone.now()
            nevent.save()
            user = nevent.email
            subject = 'Acara'+nevent.event_name+'Akan Dipertimbangkan'
            message = 'Terima kasih telah mengirim ajuan. Acara Anda akan kami pertimbangkan segera.'
            from_email = settings.EMAIL_HOST_USER
            to_list = [user, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently = True)

            return HttpResponseRedirect(reverse('public:events',))
    else :
        form = EventForm()
    context={'form':form,}
    deal_event= Event.objects.filter(event_status='deal').filter(is_publish=True)
    context["devent"] = deal_event
    return render(request, 'public/events.html', context)

@login_required
def myprofile(request):
    payment_tf = get_object_or_404(Administrasi, user = request.user, jenis__paymentstype='Registration and First Dues')
    if request.method=="POST":
        form_transfer = RegisterTransferForm(request.POST, request.FILES, instance= payment_tf)
        if form_transfer.is_valid():
            tfpayment = form_transfer.save(commit = False)
            tfpayment.save()
            bendaharas = User.objects.filter(groups__name='bendahara')
            subject = 'Pembayaran Registrasi'
            message = 'Bukti pembayaran registrasi melalui transfer oleh '+request.user.username+ ' telah diterima'
            from_email = settings.EMAIL_HOST_USER
            to_list = [settings.EMAIL_HOST_USER]
            for bendahara in bendaharas:
                to_list.append(bendahara.email)

            send_mail(subject, message, from_email, to_list, fail_silently = True)

            return HttpResponseRedirect(reverse('public:myprofile',))
    else :
        form_transfer = RegisterTransferForm(instance=payment_tf)
    context={'form_transfer':form_transfer,}
    administrasi_query = Administrasi.objects.filter(user = request.user)
    context['adminitrasis'] = administrasi_query
    regis_pay = Administrasi.objects.filter(user=request.user).filter(jenis__paymentstype='Registration and First Dues')[0]
    context['regis_payment'] = regis_pay
    today = today = timezone.now().date()
    mykelas = LogKelas.objects.filter(user=request.user)
    context['mykelas'] = mykelas

    timeline_query = Timeline.objects.all()
    context['timeline_messages'] = timeline_query
    # if request.method == 'POST':
    #     offerpayment_form = NewPaymentOfferForm(data = request.POST)
    #     if offerpayment_form.is_valid():
    #         nofferpayment = offerpayment_form.save(commit = False)
    #
    #     else:
    #         print (offerpayment_form.errors)
    # else:
    #     offerpayment_form = NewPaymentOfferForm()
    # context={'offerpayment_form' : offerpayment_form, }
    return render(request, 'public/myprofile.html', context)

def edit_user(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    if request.method == "POST":
        form_edit_profile = UserProfileEditForm(request.POST,request.FILES,  instance = user)
        if form_edit_profile.is_valid():
            userprofile = form_edit_profile.save(commit=False)
            userprofile.updated_date= timezone.now()
            userprofile.save()
            return HttpResponseRedirect(reverse('public:myprofile'))
    else:
        form_edit_profile = UserProfileEditForm(instance = user)
        return render(request, "public/edit_profile.html", {'form_edit_profile':form_edit_profile})

@has_role_decorator('tutor')
def home_tutor(request):
    context={}
    today = timezone.now().date()
    practice_query = Practice.objects.filter(date__gte=today)
    context['practices'] = practice_query
    present_query = PracticeAttendance.objects.filter(practice__date__gte=today)
    context['presents'] = present_query
    context['now'] = timezone.now().date()
    return render(request, 'public/tutor.html', context)

def permission_denied(request):
    return render(request, 'login/403.html', {})

def bad_request(request):
    return render(request, 'login/400.html', {})

def page_not_found(request):
    return render(request, 'login/404.html', {})

def server_error(request):
    return render(request, 'login/500.html', {})
