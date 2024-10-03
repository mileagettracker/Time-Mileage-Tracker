from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Simple function-based view for the homepage
def index_view(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    #path('', include('users.urls')),
    path('', index_view, name='index'),  # Root URL points to the index view
]