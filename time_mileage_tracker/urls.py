from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from time_mileage_tracker.views import home_view, user_profile
from . import views  # Assuming your views are in a views.py file



# Simple function-based view for the homepage
def index_view(request):
    return render(request, 'index.html')

urlpatterns = [
    # path('profile/', views.profile_view, name='profile'),  # This defines the 'profile' URL pattern

    path('admin/', admin.site.urls),
    path('', index_view, name='index'),  # Root URL points to the index view

    path('dashboard/', home_view, name='dashboard'),  # Root URL points to the index view

    path('login/', LoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('route/', views.route_view, name='route.html'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('user_profile/', user_profile, name='user_profile'),
]