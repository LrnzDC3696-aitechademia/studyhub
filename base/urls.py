from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='base-home'),
    path('room/<str:pk>', views.room, name='base-room'),
]
