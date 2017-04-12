from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, Practice, Administrasi
from .forms import ArticleForm, SchedulesForm
from public.models import UserProfile

@login_required
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

def home_hpd(request):
    context={}
    articles_query = Article.objects.all()
    context['articles'] = articles_query
    return render(request, 'manajemen/hpd.html', context)

def home_psdm(request):
    context={}
    user_profile = UserProfile.objects.all()
    context['userprofiles']= user_profile
    practice_query = Practice.objects.all()
    context['practices'] = practice_query
    return render(request, 'manajemen/psdm.html', context)

def home_keuangan(request):
    context={}
    administrasi_query = Administrasi.objects.all()
    context['adminitrasis']= administrasi_query
    return render(request, 'manajemen/keuangan.html', context)

def home_inventaris(request):
    context= {}
    return render(request, 'manajemen/inventaris.html', context)

def absensi_practice(request, practice_id):
    context={}
    user_query = User.objects.all()
    context['users'] = user_query
    return render(request, 'manajemen/absensi.html', context)

def detail_article(request, article_id):
    context={}
    articleid_query= Article.objects.get(id=article_id)
    context['articleid'] = articleid_query
    return render(request, 'manajemen/detail_article.html', context)

def edit_article(request, article_id):
    narticle = get_object_or_404(Article, id=article_id)
    if request.method=="POST":
        form = ArticleForm(request.POST, instance = narticle)
        if form.is_valid():
            narticle = form.save(commit = False)
            narticle.author = request.user
            narticle.updated_date= timezone.now()
            narticle.save()
            return HttpResponseRedirect(reverse('manajemen:detail_article', args=(narticle.id,)))
    else :
        form = ArticleForm(instance = narticle)
    return render(request, 'manajemen/edit_article.html', {'form':form})

def edit_schedule(request, schedule_id):
    nschedule = get_object_or_404(Practice, id=schedule_id)
    if request.method=="POST":
        form = SchedulesForm(request.POST, instance = nschedule)
        if form.is_valid():
            nschedule = form.save(commit = False)
            nschedule.created_date= timezone.now()
            nschedule.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form = SchedulesForm(instance = nschedule)
    return render(request, 'manajemen/edit_schedule.html', {'form':form})

def new_article(request):
    if request.method=="POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            narticle = form.save(commit = False)
            narticle.author = request.user
            narticle.published_date= timezone.now()
            narticle.save()
            return HttpResponseRedirect(reverse('manajemen:detail_article', args=(narticle.id,)))
    else :
        form = ArticleForm()
    return render(request, 'manajemen/edit_article.html', {'form':form})

def new_schedule(request):
    if request.method=="POST":
        form = SchedulesForm(request.POST)
        if form.is_valid():
            nschedule = form.save(commit = False)
            nschedule.created_date= timezone.now()
            nschedule.save()
            return HttpResponseRedirect(reverse('manajemen:home_psdm', ))
    else :
        form = SchedulesForm()
    return render(request, 'manajemen/edit_schedule.html', {'form':form})
