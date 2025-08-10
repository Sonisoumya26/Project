from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),           # Root page ("/")
    path('api/chat/', views.chat_api, name='chat_api'),    # AJAX POST only
]
