from django.shortcuts import render
from .models import Article

def index(request):
    context={}
    return render(request, 'manajemen/index.html', context)
def list_article(request):
    context={}
    article_query = Article.objects.all()
    context['articles'] = article_query
    return render(request, 'manajemen/list_article.html', context)
