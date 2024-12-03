import os.path

from django.contrib.auth import login, logout,authenticate
from django.http import HttpResponseRedirect, FileResponse, Http404
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.views import View
from django.http import HttpResponse, JsonResponse  
import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from .models import RouteLog
from django.contrib.auth.decorators import login_required, user_passes_test


# def profile_view(request):
#     return render(request, 'profile.html')  # Assuming you have a profile.html template

logger = logging.getLogger(__name__)


def route_view(request):
    if request.method == 'POST':
        current_location = request.POST.get('current_location')
        destination = request.POST.get('destination')
        distance = request.POST.get('distance')
        duration = request.POST.get('duration')
        print(f"Submitted Data: {current_location}, {destination}, {distance}, {duration}")

        RouteLog.objects.create(
            user=request.user,
            start_location=current_location,
            end_location=destination,
            distance=float(distance),
            duration=float(duration),
        )

        return redirect('user_profile')
    return render(request, 'route.html')

@login_required
def user_profile(request):
    username = request.user.username
    user_routes = RouteLog.objects.filter(user=request.user)
    return render(request, 'user_profile.html', {'user_routes': user_routes, 'username': username})



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
    context = {
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'dashboard.html', context)

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        # Get form data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password != password2:
            return render(request, 'registration/signup.html', {
                'error': 'Passwords do not match'
            })

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/signup.html', {
                'error': 'Username is already taken'
            })

        # Create the user
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Log the user in after successful sign-up
        login(request, user)

        # Redirect to a dashboard or home page
        return redirect('dashboard')  # Replace 'dashboard' with your actual view name

    return render(request, 'registration/signup.html')


def about_view(request):
    return render(request, 'about.html')  # Replace with your actual template

# add login required decorator to restrict access to authenticated admin

@login_required
@user_passes_test(lambda u: u.is_superuser)
def employee_reports_view(request):
    # get individual route logs
    route_logs = RouteLog.objects.all()

    return render(request, 'employee_reports.html', {'route_logs': route_logs})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def modify_report_view(request, route_log_id):
    route_log = get_object_or_404(RouteLog, id=route_log_id)
    if request.method == 'POST':
        route_log.start_location = request.POST['start_location']
        route_log.end_location = request.POST['end_location']
        route_log.distance = request.POST['distance']
        route_log.duration = request.POST['duration']
        route_log.save()
        return redirect('employee_reports')
    return render(request, 'modify_report.html', {'route_log': route_log})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def export_report_view(request, route_log_id):
    route_log = get_object_or_404(RouteLog, id=route_log_id)
    from io import BytesIO
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = [
        ['Start Location', 'End Location', 'Distance', 'Duration'],
        [route_log.start_location, route_log.end_location, f"{route_log.distance:.2f} miles",
         f"{route_log.duration:.2f} hours"]
    ]
    table = Table(data)
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                              ])
    table.setStyle(table_style)
    elements.append(table)

    doc.build(elements)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="route_log_{route_log_id}.pdf"'
    return response


@login_required
@user_passes_test(lambda u: u.is_superuser)
def export_all_reports_view(request):
    route_logs = RouteLog.objects.all()
    from io import BytesIO
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = [['Start Location', 'End Location', 'Distance', 'Duration']]
    for route_log in route_logs:
        data.append([route_log.start_location, route_log.end_location, f"{route_log.distance:.2f} miles",
                     f"{route_log.duration:.2f} hours"])

    table = Table(data)
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                              ])
    table.setStyle(table_style)
    elements.append(table)
    doc.build(elements)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_route_logs.pdf"'
    return response

# about page documentation view

def download_file(request, file_name):
    file_path = os.path.join(settings.BASE_DIR,'static','assets','pdfs', file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    else:
        raise Http404("File not found")


class CustomLoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is valid; log them in
            login(request, user)
            return redirect('dashboard')  # Replace with your desired success page
        else:
            # Check if the username exists
            from django.contrib.auth.models import User
            if not User.objects.filter(username=username).exists():
                messages.error(request, "Username not found.")
            else:
                messages.error(request, "Invalid password.")

        return render(request, 'registration/login.html')
