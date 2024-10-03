from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from .forms import SignUpForm

def login_view(request):
    # Your login view logic here
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login') # sends back to login
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})