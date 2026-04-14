from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", views.register, name="register"),
    path("create/", views.create_room, name="create_room"),
    path("room/<str:code>/", views.room_detail, name="room_detail"),
    path('join/', views.join_room, name='join_room'),
    path("login/", views.custom_login, name="login"),

]


