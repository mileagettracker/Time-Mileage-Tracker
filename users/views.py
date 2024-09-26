from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect

def login_view(request):
    # Your login view logic here
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
