from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.http import JsonResponse
import logging

from .models import RouteLog

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
        return JsonResponse({'status': 'success'})

    return render(request, 'route.html')

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
                return redirect('dashboard')  # Redirect to a home or dashboard page
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
    return render(request, 'dashboard.html')  # Replace with your actual template