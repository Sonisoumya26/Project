from django.urls import path, include

urlpatterns = [
    path('chat2/', include('chat2.urls')),   # This already exists
    path('', include('chat2.urls')),         # This adds '/' so / also routes to chat2
]