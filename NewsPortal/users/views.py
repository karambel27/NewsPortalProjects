from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from .forms import LoginForm, ProfileUserForm, RegisterFormUser


class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterUser(CreateView):
    form_class = RegisterFormUser
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация'}
