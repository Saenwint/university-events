from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views import View

from users.forms import RegistrationForm, LoginForm
from users.models import User


class RegisterView(View):
    """Регистрация нового пользователя."""
    template_name = 'registration/register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_confirmed = False
            user.save()
            login(request, user)
            return redirect('profile', id=user.id)
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """Вход пользователя."""
    template_name = 'registration/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile', id=user.id)
            else:
                form.add_error(None, "Неверный email или пароль")
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Выход пользователя."""
    def get(self, request):
        logout(request)
        return redirect('login')


def profile_view(request, id):
    """Профиль пользователя по ID."""
    user = get_object_or_404(User, id=id)
    return render(request, 'profile.html', {'user': user})