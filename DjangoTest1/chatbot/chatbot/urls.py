from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat2.urls')),    # Only routes to chat2 app at root (/)
]
