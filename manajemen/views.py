from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Article
from .forms import ArticleForm


def index(request):
    context={}
    return render(request, 'manajemen/index.html', context)

def list_article(request):
    context={}
    articles_query = Article.objects.all()
    context['articles'] = articles_query
    return render(request, 'manajemen/list_article.html', context)

def detail_article(request, article_id):
    context={}
    articleid_query= Article.objects.get(id=article_id)
    context['articleid'] = articleid_query
    return render(request, 'manajemen/detail_article.html', context)

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
