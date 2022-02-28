from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='base-home'),
    path('room/', views.room, name='base-room'),
]
