from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def user_login(request):
    logged_in = True
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('public:index'))


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password )
        print('user', user)
        if user:
            if user.is_active:
                login(request, user)
                if user.profile.tipe_user == 'member':
                    return HttpResponseRedirect(reverse('public:index'))
                else:
                    return HttpResponseRedirect(reverse('manajemen:index'))

            else:
                logged_in = False
                return render(request, 'login/login.html', {"logged_in": logged_in})
        else:
            print ("Invalid login details: {0},{1}".format(username, password))
            logged_in = False
            return render(request, 'login/login.html', {"logged_in": logged_in})
    else:
        return render(request, 'login/login.html', {"logged_in": logged_in})

def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are Logged in.")
    else:
        return HttpResponse("You are not Logged in.")

def permission_denied(request):
    return render(request, 'login/403.html', {})

def bad_request(request):
    return render(request, 'login/400.html', {})

def page_not_found(request):
    return render(request, 'login/404.html', {})

def server_error(request):
    return render(request, 'login/500.html', {})

@login_required
def restricted(request):
    return HttpResponse("since you're logged in, you can see this text!")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('public:index'))

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('public:myprofile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'login/change_password.html', {
        'form': form
    })

def permission_denied(request):
    return render(request, 'login/403.html', {})

def bad_request(request):
    return render(request, 'login/400.html', {})

def page_not_found(request):
    return render(request, 'login/404.html', {})

def server_error(request):
    return render(request, 'login/500.html', {})
