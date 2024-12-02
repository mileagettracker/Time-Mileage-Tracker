from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.http import HttpResponse, JsonResponse  
from django.contrib.auth.decorators import login_required
import logging

from .models import RouteLog, Signup


# def profile_view(request):
#     return render(request, 'profile.html')  # Assuming you have a profile.html template

logger = logging.getLogger(__name__)

def route_view(request):
    if request.method == 'POST':
        current_location = request.POST.get('current_location')
        destination = request.POST.get('destination')
        distance = request.POST.get('distance')
        duration = request.POST.get('duration')
        print("route_view")
        print(f"Submitted Data: {current_location}, {destination}, {distance}, {duration}")


        RouteLog.objects.create(
            user=request.user,
            start_location=current_location,
            end_location=destination,
            distance=float(distance),
            duration=float(duration),
        )
        return render(request, 'user_profile.html')

    return render(request, 'route.html')

@login_required
def user_profile(request):
    user_routes = RouteLog.objects.filter(user=request.user)
    print(user_routes)
    return render(request, 'user_profile.html', {'user_routes': user_routes})





def login_view(request):
    if request.method == 'POST':
        # Handle POST request: Process the login form data
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard page
            else:
                return HttpResponse("Invalid login")
        else:
            return HttpResponse("Invalid form data")
    else:
        # Handle GET request: Display the login form
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def home_view(request):
    return render(request, 'dashboard.html')

@login_required
def user_view(request):
    username = request.user.username
    return render(request, 'user_profile.html', {'username': username})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Signup.objects.create(
                user=request.user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                password=user.set_password,  # Password is already hashed
            )
            return redirect('login') # Redirect to login page
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})