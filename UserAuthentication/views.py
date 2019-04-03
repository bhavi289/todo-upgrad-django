from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

def SignUp(request):
    if request.method == "GET":
        save = None
        if request.GET.get('save'):
            save = int(request.GET.get('save'))
        return render(request, 'UserAuthentication/sign-up.html', {'save':save})
    if request.method == "POST":
        try:
            with transaction.atomic():
                username = request.POST.get('username')
                email = request.POST.get('email')
                password = request.POST.get('password')

                user = User()
                user.username = username
                user.set_password(password)
                user.email = email
                user.save()
                return HttpResponseRedirect(reverse("UserAuthentication:Login")+"?save=1")
                # return HttpResponse("Successfully Created")
        except Exception as e:
            print (e)
            return HttpResponseRedirect(reverse("UserAuthentication:SignUp")+"?save=0")
            # return HttpResponse("Some Error Occured")

def Login(request):
    if request.method == "GET":
        save = None
        if request.GET.get('save'):
            save = int(request.GET.get('save'))
        return render(request, 'UserAuthentication/login.html', {'save':save})
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("Schedule:Home"))
        return HttpResponseRedirect(reverse("UserAuthentication:Login")+"?save=0")
        # return HttpResponse("Wrong Credentials")
