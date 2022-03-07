from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='base-home'),

    path("login/", views.login_page, name="base-login"),
    path("logout/", views.logout_user, name="base-logout"),
    path("register/", views.register_page, name="base-register"),

    path('profile/<str:pk>', views.user_profile, name='base-user_profile'),
    path('update_user/', views.update_user, name='base-update_user'),

    path('room/<str:pk>', views.room, name='base-room'),
    path("create_room/", views.create_room, name="base-create_room"),
    path("update_room/<str:pk>", views.update_room, name="base-update_room"),
    path("delete_room/<str:pk>", views.delete_room, name="base-delete_room"),
    path("delete_message/<str:pk>", views.delete_message, name="base-delete_message"),

    path('topics/', views.topic_page, name="base-topics"),
    path('activity/', views.activity_page, name="base-activity")
]
