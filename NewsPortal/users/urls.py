from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path("login/", views.LoginUserView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("profile/", views.ProfileUser.as_view(), name='profile'),
    path("statauthor/", views.statauthor, name='statauthor'),

    # path("register/", views.RegisterUser.as_view(), name='register'),


]
