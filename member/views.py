from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from manajemen.models import Administrasi, PracticeAttendance

# Create your views here.
@login_required
def index(request):
    if request.user.profile.tipe_user != 'member':
        return HttpResponseRedirect(reverse('manajemen:index'))
    context={}
    return render(request, 'member/index.html', context)

def latihan(request):
    context={}
    present_query = PracticeAttendance.objects.filter(is_present = request.user)
    context['presents'] = present_query
    return render(request, 'member/latihan.html', context)

def pembayaran(request):
    context={}
    administrasi_query = Administrasi.objects.filter(user = request.user)
    #add kondisi sesuai dengan username yang aktif
    context['adminitrasis']= administrasi_query
    return render(request, 'member/pembayaran.html', context)

def settings(request):
    context={}
    return render(request, 'member/pengaturan.html', context)
