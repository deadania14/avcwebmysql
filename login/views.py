from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def user_login(request):
    logged_in = True
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password )
        print('user', user)
        if user:
            if user.is_active:
                login(request, user)
                if user.profile.tipe_user == 'member':
                    return HttpResponseRedirect(reverse('member:index'))
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

@login_required
def restricted(request):
    return HttpResponse("since you're logged in, you can see this text!")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('public:index'))
