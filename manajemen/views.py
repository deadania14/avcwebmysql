from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import Article, Practice, Administrasi, Kelas, PracticeAttendance, Inventory, Meeting, AdministrationType, LogKelas
from .forms import ArticleForm, MainArticleForm, SchedulesForm, EditUserClassForm, AbsensiForm, AbsensiPeopleForm, AVCContactForm, NewEventForm, EditBarangForm, AbsensiKelasForm, EditUser, NewMeetingForm, EditMeetingForm, NewBarangForm, EditEventForm, NewPaymentForm, EditPaymentForm, NewClassForm, NewPaymentTypeForm, EditPaymentTypeForm, NewBroadcastMessageForm
from public.models import UserProfile, Event, SettingsVariable, Timeline
from rolepermissions.decorators import has_role_decorator

@login_required
@has_role_decorator('manajemen')
def index(request):
    context={}
    member_user_query = UserProfile.objects.filter(tipe_user='member').filter(user__is_active=True)
    context['members'] = member_user_query
    #belom kelar
    new_member_query = UserProfile.objects.filter(tipe_user='member')
    context['new_members'] = new_member_query
    inventory_query = Inventory.objects.all()
    context['inventories']= inventory_query
    tutor_user_query = UserProfile.objects.filter(tipe_user='tutor')
    context['tutors'] = tutor_user_query
    manajemen_user_query = UserProfile.objects.filter(user__groups__name='manajemen')
    context['manajemens']=manajemen_user_query
    rapat_query = Meeting.objects.all()
    context['meetings'] = rapat_query
    return render(request, 'manajemen/index.html', context)

@has_role_decorator('sekretaris')
def home_sekretaris(request):
    context={}
    user_profile = UserProfile.objects.all()
    context['userprofiles']= user_profile
    meeting_query = Meeting.objects.all()
    context['meetings']= meeting_query
    return render(request, 'manajemen/sekretaris.html', context)

def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    subject = 'Status Akun Anda'
    message = message = render_to_string('messages/akun.html', {
    'user' : user,
    'status': 'tidak aktif',
    'sender': 'Alliance Violin Community Depok Official',
    })
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [user.email])
    return HttpResponseRedirect(reverse('manajemen:home_sekretaris'))

def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    subject = 'Status Akun Anda'
    message = message = render_to_string('messages/akun.html', {
    'user' : user,
    'status': 'aktif',
    'sender': 'Alliance Violin Community Depok Official',
    })
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [user.email])
    return HttpResponseRedirect(reverse('manajemen:home_sekretaris'))

def new_meeting(request):
    if request.method=="POST":
        form_new_meeting = NewMeetingForm(request.POST)
        print(form_new_meeting)
        if form_new_meeting.is_valid():
            nmeeting = form_new_meeting.save(commit=False)
            nmeeting.created_date= timezone.now()
            form_new_meeting.save_m2m()
            cek_practice_date = Meeting.objects.filter(date_meet=nmeeting.date_meet)
            if cek_practice_date:
                form_new_meeting.add_error('date_meet', u"Catatan Sudah Ada")
                return render(request, 'manajemen/new_meeting.html', {'form_new_meeting':form_new_meeting})
            nmeeting.save()
            return HttpResponseRedirect(reverse('manajemen:home_sekretaris', ))
    else :
        form_new_meeting = NewMeetingForm()
    return render(request, 'manajemen/new_meeting.html', {'form_new_meeting':form_new_meeting})

def edit_meeting(request, meeting_id):
    context={}
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method=="POST":
        form_edit_meeting = EditMeetingForm(request.POST, instance = meeting)
        if form_edit_meeting.is_valid():
            meeting = form_edit_meeting.save(commit = False)
            meeting.updated_date= timezone.now()
            form_edit_meeting.save_m2m()
            meeting.save()
            return HttpResponseRedirect(reverse('manajemen:home_sekretaris', ))
    else :
        form_edit_meeting = EditMeetingForm(instance = meeting)
    return render(request, 'manajemen/edit_meeting.html', {'form_edit_meeting':form_edit_meeting})

def delete_meeting(request, meeting_id):
    meeting_query = Meeting.objects.get(id=meeting_id)
    meeting_query.delete()
    return HttpResponseRedirect(reverse('manajemen:home_sekretaris'))

@has_role_decorator('bendahara')
def home_bendahara(request):
    context={}
    administrasi_type_query = AdministrationType.objects.all()
    context['adminitrasi_tipe']= administrasi_type_query
    administrasi_query = Administrasi.objects.all()
    context['adminitrasis']= administrasi_query
    context['saldo'] = Administrasi.saldo.get_saldo()
    return render(request, 'manajemen/keuangan.html', context)

def new_administration_type(request):
    if request.method=="POST":
        form_new_payment_type = NewPaymentTypeForm(request.POST)
        if form_new_payment_type.is_valid():
            npaymentipe = form_new_payment_type.save(commit = False)
            npaymentipe.created_date= timezone.now()
            npaymentipe.save()
            return HttpResponseRedirect(reverse('manajemen:home_keuangan', ))
    else :
        form_new_payment_type = NewPaymentTypeForm()
    return render(request, 'manajemen/new_payment_type.html', {'form_new_payment_type':form_new_payment_type})

def edit_administration_type(request, payment_type_id):
    edpaymentipe = get_object_or_404(AdministrationType, id=payment_type_id)
    if request.method=="POST":
        form_edit_payment_type= EditPaymentTypeForm(request.POST, instance = edpaymentipe)
        if form_edit_payment_type.is_valid():
            edpaymentipe = form_edit_payment_type.save(commit = False)
            edpaymentipe.updated_date= timezone.now()
            edpaymentipe.save()
            return HttpResponseRedirect(reverse('manajemen:home_keuangan', ))
    else :
        form_edit_payment_type = EditPaymentTypeForm(instance = edpaymentipe)
    return render(request, 'manajemen/edit_payment_type.html', {'form_edit_payment_type':form_edit_payment_type})

def new_pembayaran(request):
    if request.method=="POST":
        form_new_payment = NewPaymentForm(request.POST)
        if form_new_payment.is_valid():
            npayment = form_new_payment.save(commit = False)
            npayment.nominal = npayment.jenis.nominal
            npayment.created_date= timezone.now()
            npayment.save()
            from_email = settings.EMAIL_HOST_USER
            subject = 'Status Pembayaran '+ payment.jenis.paymentstype +' a/n '+payment.user
            message = 'Pembayaran '+ payment.jenis.paymentstype  +'Anda telah berhasil dikonfirmasi. Salam Gesek Selalu by AVC'
            send_mail(subject, message, from_email, [npayment.profile.email])
            return HttpResponseRedirect(reverse('manajemen:home_keuangan', ))
    else :
        form_new_payment = NewPaymentForm()
    return render(request, 'manajemen/new_payment.html', {'form_new_payment':form_new_payment})

def confirmation_payment(request, payment_id):
    payment = Administrasi.objects.get(id=payment_id)
    payment.status = "paid"
    payment.save()
    from_email = settings.EMAIL_HOST_USER
    if payment.jenis.paymentstype == 'Registration and First Dues':
        userp = User.objects.get(username = payment.user)
        userp.profile.is_registration_paid = True
        userp.profile.save()
        subject = 'Pendaftaran '+ str(userp.username) +' berhasil'
        message = render_to_string('login/welcome.html', {
        'user': userp,
        })
        send_mail(subject, message, from_email, [userp.email])
    else :
        userp = User.objects.get(username = payment.user)
        subject = 'Status Pembayaran '+ payment.jenis.paymentstype +' a/n '+ str(userp.username)
        message = 'Pembayaran '+ payment.jenis.paymentstype  +'Anda telah berhasil dikonfirmasi. Salam Gesek Selalu by AVC'
        send_mail(subject, message, from_email, [userp.email])
    subject = 'Pemberitahuan konfirmasi pembayaran'
    message = render_to_string('messages/verifikasitindakan.html', {
    'user': userp,
    'tindakan': 'konfirmasi penerimaan pembayaran '+ payment.jenis.paymentstype +' a/n ',
    'userlogged': request.user,
    })
    send_mail(subject, message, from_email, [userp.email])
    return HttpResponseRedirect(reverse('manajemen:home_keuangan'))

def cancel_payment(request, payment_id):
    payment = Administrasi.objects.get(id=payment_id)
    payment.status = "cancelled"
    payment.save()
    if payment.jenis.paymentstype == 'Registration and First Dues':
        payment.user.is_active = False
        payment.user.save()
    from_email = settings.EMAIL_HOST_USER
    userp = User.objects.get(username = payment.user)
    subject = 'Status Pembayaran '+ payment.jenis.paymentstype +' a/n '+str(userp.username)
    message = 'Pembayaran '+ payment.jenis.paymentstype  +'Anda telah digagalkan. Salam Gesek Selalu by AVC.'
    send_mail(subject, message, from_email, [userp.email])
    return HttpResponseRedirect(reverse('manajemen:home_keuangan'))

@has_role_decorator('psdm')
def home_psdm(request):
    context={}
    today = timezone.now().date()
    user_profile = UserProfile.objects.all()
    context['userprofiles']= user_profile
    practice_query = Practice.objects.order_by('-date')
    context['practices'] = practice_query
    kelas_query = Kelas.objects.all()
    context['classes'] = kelas_query
    present_query = PracticeAttendance.objects.all()
    context['presents'] = present_query
    context['now'] = today
    return render(request, 'manajemen/psdm.html', context)

def move_class(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    today = timezone.now().date()
    kelasbefore = user.user_kelas
    if request.method=="POST":
        form_move_user = EditUserClassForm(request.POST, instance=user)
        if form_move_user.is_valid():
            moveuser = form_move_user.save(commit = False)
            logkelas = LogKelas.objects.create(kelas_current=moveuser.user_kelas, user=moveuser.user,
                kelas_before=kelasbefore, joined_date= today)
            moveuser.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form_move_user = EditUserClassForm(instance=user)
    return render(request, 'manajemen/move_user_class.html', {'form_move_user':form_move_user})

def new_kelas(request):
    if request.method=="POST":
        form_new_kelas = NewClassForm(request.POST)
        if form_new_kelas.is_valid():
            nclass = form_new_kelas.save(commit = False)
            nclass.updated_date= timezone.now()
            nclass.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form_new_kelas = NewClassForm()
    return render(request, 'manajemen/new_class.html', {'form_new_kelas':form_new_kelas})

def new_schedule(request):
    if request.method=="POST":
        form_edit_schedule = SchedulesForm(request.POST)
        print(form_edit_schedule)
        if form_edit_schedule.is_valid():
            nschedule = form_edit_schedule.save(commit = False)
            nschedule.created_date = timezone.now()
            nschedule.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form_edit_schedule = SchedulesForm()
    return render(request, 'manajemen/edit_schedule.html', {'form_edit_schedule':form_edit_schedule})

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

def delete_schedule(request, schedule_id):
    practice_query = Practice.objects.get(id=schedule_id)
    practice_query.delete()
    return HttpResponseRedirect(reverse('manajemen:home_psdm'))

def edit_attendance(request, attendance_id):
    npresent = get_object_or_404(PracticeAttendance, id=attendance_id)
    if request.method=="POST":
        form_edit_absensi = AbsensiForm(request.POST, instance = npresent)
        if form_edit_absensi.is_valid():
            form_edit_absensi.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form_edit_absensi = AbsensiForm(instance = npresent)
    form_edit_absensi.fields['is_present'].queryset = npresent.daftar_orang.all()
    form_edit_absensi.fields['tutor_pendamping'].queryset = User.objects.filter(profile__tipe_user='tutor').exclude(id=npresent.tutor.id).exclude(profile__user_kelas=npresent.kelas)
    return render(request, 'manajemen/edit_attendance.html', {'form_edit_absensi':form_edit_absensi, 'tutor': npresent.tutor})

def new_attendance_kelas(request):
    if request.method=="POST":
        form_absensi_kelas = AbsensiKelasForm(request.POST)
        print(request.POST.getlist('daftar_orang'))
        if form_absensi_kelas.is_valid():
            npresent = form_absensi_kelas.save(commit=False)
            npresent.updated_date= timezone.now()
            cek_practice_date = PracticeAttendance.objects.filter(practice__date=npresent.practice.date, kelas__nama_kelas= npresent.kelas)
            if cek_practice_date:
                form_absensi_kelas.add_error('kelas', u"Absensi sudah ada")
                return render(request, 'manajemen/new_attendance_kelas.html', {'form_absensi_kelas':form_absensi_kelas})
            npresent.save()
            return HttpResponseRedirect(reverse('manajemen:new_attendance_people', kwargs={'attendance_id':npresent.id}))
    else :
        form_absensi_kelas = AbsensiKelasForm()
    form_absensi_kelas.fields['practice'].queryset = Practice.objects.filter(date__gte=timezone.now().date())
    form_absensi_kelas.fields['tutor'].queryset = User.objects.filter(profile__tipe_user='tutor')
    return render(request, 'manajemen/new_attendance_kelas.html', {'form_absensi_kelas':form_absensi_kelas,})

def new_attendance_people(request, attendance_id):
    practice_attendance = get_object_or_404(PracticeAttendance, id=attendance_id)
    if request.method=="POST":
        form_absensi_people = AbsensiPeopleForm(request.POST , instance=practice_attendance)
        form_absensi_people.fields['daftar_orang'].queryset = User.objects.filter(profile__user_kelas=practice_attendance.kelas).exclude(id=practice_attendance.tutor.id)
        print(request.POST.getlist('daftar_orang'))
        if form_absensi_people.is_valid():
            npresent = form_absensi_people.save(commit=False)
            form_absensi_people.save_m2m()
            npresent.updated_date= timezone.now()
            npresent.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form_absensi_people = AbsensiPeopleForm(instance=practice_attendance)
    form_absensi_people.fields['daftar_orang'].queryset = User.objects.filter(profile__user_kelas=practice_attendance.kelas).exclude(id=practice_attendance.tutor.id)
    return render(request, 'manajemen/new_attendance_people.html', {'form_absensi_people':form_absensi_people, 'tutor': practice_attendance.tutor})

def delete_attendance(request, attendance_id):
    absensi_query = PracticeAttendance.objects.get(id=attendance_id)
    absensi_query.delete()
    return HttpResponseRedirect(reverse('manajemen:home_psdm'))

@has_role_decorator('program')
def home_program(request):
    check_event_expired()
    check_event_finish()
    context={}
    acara_query = Event.objects.all()
    context['acaras']= acara_query
    today = timezone.now().date()
    return render(request, 'manajemen/acara.html', context)

def check_event_expired():
    today = timezone.now().date()
    acara_query= Event.objects.filter(event_status="waiting", event_date__lt= today)
    for acara in acara_query:
        acara.event_status = 'cancelled'
        acara.save()

def check_event_finish():
    today = timezone.now().date()
    acara_query= Event.objects.filter(event_status="deal", event_date__lt= today)
    for acara in acara_query:
        acara.event_status = 'done'
        acara.save()

def new_event(request):
    context={}
    today = timezone.now().date()
    deal_event= Event.objects.all()
    context["devent"] = deal_event
    if request.method=="POST":
        form_new_event = NewEventForm(request.POST, request.FILES)
        if form_new_event.is_valid():
            nevent = form_new_event.save(commit = False)
            nevent.corporate = "AVC"
            nevent.sender = request.user
            nevent.event_status = "deal"
            nevent.created_date= today
            nevent.save()
            #membuat artikel dari event yang telah dikonfirmasi
            eventarticle = Article.objects.create(author = request.user, title = nevent.event_name,
            text = nevent.desc, image = nevent.image, is_event = True,  created_date = nevent.created_date)
            return HttpResponseRedirect(reverse('manajemen:home_acara', ))
    else :
        form_new_event = NewEventForm()
    return render(request, 'manajemen/new_event.html', {'form_new_event':form_new_event}, context)

def edit_event(request, event_id):
    context={}
    edevent = get_object_or_404(Event, id=event_id)
    if request.method=="POST":
        form_edit_event = EditEventForm(request.POST, request.FILES, instance = edevent)
        if form_edit_event.is_valid():
            edevent = form_edit_event.save(commit = False)
            edevent.updated_date= timezone.now()
            edevent.save()
            return HttpResponseRedirect(reverse('manajemen:home_acara', ))
    else :
        form_edit_event = EditEventForm(instance = edevent)
    return render(request, 'manajemen/edit_event.html', {'form_edit_event':form_edit_event})

def confirmation_event(request, event_id):
    today = timezone.now().date()
    eventconf = Event.objects.get(id=event_id)
    eventconf.event_status = "deal"
    eventconf.save()
    #membuat artikel dari event yang telah dikonfirmasi
    eventarticle = Article.objects.create(author = request.user, title = eventconf.event_name,
    text = eventconf.desc, image = eventconf.image, is_event = True,  created_date = today)
    from_email = settings.EMAIL_HOST_USER
    subject = 'Keputusan Partisipasi dalam Acara '+eventconf.event_name
    message = render_to_string('messages/acara.html', {
    'sender': eventconf.sender,
    'status': 'menerima',
    'event': eventconf.event_name,
    })
    send_mail(subject, message, from_email, [eventconf.email])
    return HttpResponseRedirect(reverse('manajemen:home_acara'))

def cancel_event(request, event_id):
    eventconf = Event.objects.get(id=event_id)
    eventconf.event_status = "cancelled"
    eventconf.save()
    from_email = settings.EMAIL_HOST_USER
    subject = 'Keputusan Partisipasi dalam Acara '+eventconf.event_name
    message = render_to_string('messages/acara.html', {
    'sender': eventconf.sender,
    'status': 'menunda',
    'event': eventconf.event_name,
    })
    send_mail(subject, message, from_email, [eventconf.email])
    return HttpResponseRedirect(reverse('manajemen:home_acara'))

def delete_event(request, event_id):
    event_query = Event.objects.get(id=event_id)
    event_query.delete()
    return HttpResponseRedirect(reverse('manajemen:home_acara'))

@has_role_decorator('inventaris')
def home_inventaris(request):
    context={}
    inventory_query = Inventory.objects.all()
    context['inventories']= inventory_query
    return render(request, 'manajemen/inventaris.html', context)

def new_barang(request):
    if request.method=="POST":
        form_new_barang = NewBarangForm(request.POST)
        if form_new_barang.is_valid():
            nbarang = form_new_barang.save(commit = False)
            nbarang.updated_date= timezone.now()
            nbarang.save()
            return HttpResponseRedirect(reverse('manajemen:home_inventaris'))
    else :
        form_new_barang = NewBarangForm()
    return render(request, 'manajemen/new_barang.html', {'form_new_barang':form_new_barang})

def edit_barang(request, barang_id):
    context={}
    barang = get_object_or_404(Inventory, id=barang_id)
    context['stuff_name']=barang.thingsname
    if request.method=="POST":
        form_edit_barang = EditBarangForm(request.POST, instance = barang)
        if form_edit_barang.is_valid():
            barang = form_edit_barang.save(commit = False)
            barang.updated_date= timezone.now()
            barang.save()
            return HttpResponseRedirect(reverse('manajemen:home_inventaris', ))
    else :
        form_edit_barang = EditBarangForm(instance = barang)
    context['form_edit_barang']=form_edit_barang
    return render(request, 'manajemen/edit_barang.html', context)

def delete_barang(request, barang_id):
    barang_query = Inventory.objects.get(id=barang_id)
    barang_query.delete()
    return HttpResponseRedirect(reverse('manajemen:home_inventaris'))

@has_role_decorator('hpd')
def home_hpd(request):
    if request.method == 'POST':
        message_form = NewBroadcastMessageForm(data = request.POST)
        if message_form.is_valid():
            nmessage = message_form.save(commit=False)
            nmessage.created_date = timezone.now()
            nmessage.writer = request.user
            nmessage.save()
        else:
            print (message_form.errors)
    else:
        message_form = NewBroadcastMessageForm()
    context={'message_form' : message_form,}
    articles_query = Article.objects.all()
    context['articles'] = articles_query
    broadcast_query = Timeline.objects.all()
    context['messages'] = broadcast_query
    return render(request, 'manajemen/hpd.html', context)

def new_article(request):
    if request.method=="POST":
        form_edit_article = ArticleForm(request.POST, request.FILES)
        if form_edit_article.is_valid():
            narticle = form_edit_article.save(commit = False)
            narticle.author = request.user
            narticle.updated_date= timezone.now()
            narticle.published_date= timezone.now()
            narticle.save()
            return HttpResponseRedirect(reverse('manajemen:detail_article', args=(narticle.id,)))
        else:
            print (form_edit_article.errors)
    else :
        form_edit_article = ArticleForm()
    return render(request, 'manajemen/new_article.html', {'form_edit_article':form_edit_article})

def edit_article(request, article_id):
    narticle = get_object_or_404(Article, id=article_id)
    if request.method=="POST":
        form_edit_article = ArticleForm(request.POST, request.FILES, instance = narticle)
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
        form_main_edit_article = MainArticleForm(request.POST, instance = narticle)
        if form_main_edit_article.is_valid():
            narticle = form_main_edit_article.save(commit = False)
            narticle.author = request.user
            narticle.updated_date= timezone.now()
            narticle.save()
            return HttpResponseRedirect(reverse('manajemen:detail_article', args=(narticle.id,)))
    else :
        form_main_edit_article = MainArticleForm(instance = narticle)
    return render(request, 'manajemen/edit_main_article.html', {'form_main_edit_article':form_main_edit_article})

def delete_article(request, article_id):
    article_query = Article.objects.get(id=article_id)
    article_query.delete()
    return HttpResponseRedirect(reverse('manajemen:home_hpd'))

def detail_article(request, article_id):
    context={}
    articleid_query= get_object_or_404(Article, id=article_id)
    context['articleid'] = articleid_query
    return render(request, 'manajemen/detail_article.html', context)

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

def permission_denied(request):
    return render(request, 'login/403.html', {})

def bad_request(request):
    return render(request, 'login/400.html', {})

def page_not_found(request):
    return render(request, 'login/404.html', {})

def server_error(request):
    return render(request, 'login/500.html', {})
