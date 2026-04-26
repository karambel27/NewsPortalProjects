from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from News.models import Author
from .forms import LoginForm, ProfileUserForm, RegisterFormUser


class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Профиль пользователя'
        context['author_prov'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def statauthor(request):
    user = request.user
    author_profile, _ = Author.objects.get_or_create(user=user)
    group_authors = Group.objects.get(name='authors')

    if not user.groups.filter(name='authors').exists():
        user.groups.add(group_authors)

    return redirect(request.META.get('HTTP_REFERER'))



# class RegisterUser(CreateView):
#     form_class = RegisterFormUser
#     template_name = 'users/register.html'
#     success_url = reverse_lazy('users:login')
#     extra_context = {'title': 'Регистрация'}
#
#     def form_valid(self, form):
#         user = form.save()
#         common_group = Group.objects.get(name='common')
#         user.groups.add(common_group)
#         return super().form_valid(form)
