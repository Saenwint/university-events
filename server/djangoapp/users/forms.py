from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from users.models import User


class RegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя."""
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 
            'last_name', 'password1', 
            'password2',
        ]


class LoginForm(forms.Form):
    """Форма для входа пользователя."""
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Текущий пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )