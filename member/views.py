from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
@login_required
def index(request):
    if request.user.profile.tipe_user != 'member':
        return HttpResponseRedirect(reverse('manajemen:index'))
    context={}
    return render(request, 'member/index.html', context)

def latihan(request):
    context={}
    return render(request, 'member/latihan.html', context)

def pembayaran(request):
    context={}
    return render(request, 'member/pembayaran.html', context)

def contact(request):
    context={}
    return render(request, 'member/kontak.html', context)
