from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from . import views




# Simple function-based view for the homepage
def index_view(request):
    return render(request, 'index.html')

urlpatterns = [
    # path('profile/', views.profile_view, name='profile'),  # This defines the 'profile' URL pattern

    path('admin/', admin.site.urls),
    path('', index_view, name='index'),  # Root URL points to the index view

    path('dashboard/', views.home_view, name='dashboard'),  # Root URL points to the index view

     path('login/', LoginView.as_view(), name='login'),

    path('route/', views.route_view, name='route.html'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # admin page
    path('report/', views.employee_reports_view, name='employee_reports'),
    path('modify-report/<int:route_log_id>/', views.modify_report_view, name='modify_report'),
    path('export-report/<int:route_log_id>/', views.export_report_view, name='export_report'),
    path('export-all-reports/', views.export_all_reports_view, name='export_all_reports'),
    # about page
    path('about/', views.about_view, name='about'),
    path('downoald/<str:file_name>/', views.download_file, name='download_file'),


]