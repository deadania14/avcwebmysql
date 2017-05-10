from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from manajemen.models import Administrasi, PracticeAttendance, Kelas
from public.models import UserProfile, Event
from .forms import UserProfileForm

# Create your views here.
@login_required
def index(request):
    if request.user.profile.tipe_user != 'member':
        return HttpResponseRedirect(reverse('manajemen:index'))
    context={}
    administrasi_query = Administrasi.objects.filter(user = request.user)
    #add kondisi sesuai dengan username yang aktif
    context['adminitrasis'] = administrasi_query
    kelas_query = Kelas.objects.filter(user= request.user)
    context['kelas'] = kelas_query
    today = today = timezone.now().date()
    events_query = Event.objects.filter(event_status="deal").filter(event_date__gte=today)
    context['events'] = events_query
    return render(request, 'member/index.html', context)

def edit_user(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserProfileForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('phone', 'address', 'photo'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect(reverse('member:index'))

        return render(request, "member/edit_profile.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
