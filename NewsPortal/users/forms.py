import datetime

from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(), label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    time_yeld = datetime.date.today().year
    data_bird = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(time_yeld - 80, time_yeld - 5))))
    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'data_bird', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }


class RegisterFormUser(UserCreationForm):
    username = forms.CharField(max_length=100, label='Логин')
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(), label="Пароль")
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(), label="Повтор пароля")

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {'email': 'E-mail',
                  'first_name': 'Имя',
                  'last_name': 'Фамилия'}

    def clean_email(self):
        if get_user_model().objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError('Этот E-mail уже зарегистрирован')
        return self.cleaned_data['email']


class MyCustomSignupForm(SignupForm):

    def save(self, request):
        user = super().save(request)
        common_group = Group.objects.get(name='common')
        user.groups.add(common_group)
        return user
