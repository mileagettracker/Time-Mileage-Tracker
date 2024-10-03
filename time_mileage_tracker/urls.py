from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from time_mileage_tracker.views import home_view


# Simple function-based view for the homepage
def index_view(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('regisration/', include('users- DNU.urls')),
    path('', index_view, name='index'),  # Root URL points to the index view

    path('home/', home_view, name='home'),  # Root URL points to the index view

     path('login/', LoginView.as_view(), name='login'),
    path('', home_view, name='home'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]