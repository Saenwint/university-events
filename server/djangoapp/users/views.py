from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from users.forms import RegistrationForm, LoginForm, ChangePasswordForm
from users.models import User
from users import utils
from users.tokens import generate_token
from tickets.models import Ticket


class RegisterView(View):
    """Регистрация нового пользователя с подтверждением email."""
    template_name = 'users/registration/register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            pass1 = form.cleaned_data.get('password1')
            pass2 = form.cleaned_data.get('password2')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Этот email уже зарегистрирован!")
                return redirect('users:register')

            if pass1 != pass2:
                messages.error(request, "Пароли не совпадают!")
                return redirect('users:register')
            
            user = form.save(commit=False)
            user.is_confirmed = False
            user.is_active = True
            user.save() 
            
            try:
                mail = utils.send_confirmation_email(request=request, user=user)
                if not mail:
                    messages.error(request, "Не удалось отправить email")
                    return redirect('users:register')
                
                messages.success(
                    request,
                    'Регистрация успешна! Проверьте email для подтверждения. '
                    'Вы сможете войти после подтверждения email.'
                )
                return redirect('users:login')
                
            except Exception as e:
                messages.error(
                    request,
                    f'Ошибка при отправке письма: {str(e)}. Попробуйте позже.'
                )
                return redirect('users:register')
                
        return render(request, self.template_name, {'form': form})
    

class ConfirmEmailView(View):
    template_name = 'users/emails/email_confirmed.html'
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError) as e:
            messages.error(f"UID decode error: {e}")
            user = None
        except User.DoesNotExist:
            messages.error(f"User not found for UID: {uid}")
            user = None

        if user is None:
            messages.error(request, "Неверная ссылка подтверждения.")
            return redirect('users:login')
        
        if generate_token.check_token(user, token):
            user.is_confirmed = True
            user.save()
            messages.success(request, 'Email успешно подтверждён!')
            login(request, user)
            return redirect('users:profile')
        else:
            messages.error(request, "Ссылка устарела или недействительна.")
            return redirect('users:login')


class LoginView(View):
    """Вход пользователя."""
    template_name = 'users/registration/login.html'

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
                return redirect('users:profile')
            else:
                form.add_error(None, "Неверный email или пароль")
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    """Выход пользователя."""
    login_url = '/users/login/'
    def get(self, request):
        logout(request)
        return redirect('users:login')


class ProfileView(LoginRequiredMixin, View):
    """Профиль пользователя по ID."""
    login_url = '/users/login/'
    template_name = 'users/profile/profile.html'

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})
    

class UserEventsView(LoginRequiredMixin, View):
    """Мероприятия, на которые зарегестрировался пользователь"""
    login_url = '/users/login/'
    template_name = 'users/profile/user_events.html'

    def get(self, request):
        user = request.user
        tickets = Ticket.objects.filter(user=user).select_related('event').order_by('-registration_date')
        
        return render(request, self.template_name, {
            'tickets': tickets,
        })
    

class UserSettings(LoginRequiredMixin, View):
    """Настройки пользователя"""
    login_url = '/users/login/'
    template_name = 'users/profile/settings.html'

    def get(self, request):
        password_form = ChangePasswordForm(user=request.user)
        return render(request, self.template_name, {
            'password_form': password_form,
            'user': request.user
        })

    def post(self, request):
        if 'resend_confirmation' in request.POST:
            return self.resend_confirmation(request)
        elif 'change_password' in request.POST:
            return self.change_password(request)
        return redirect('users:settings')

    def resend_confirmation(self, request):
        user = request.user
        if user.is_confirmed:
            messages.info(request, "Ваш email уже подтвержден")
            return redirect('users:settings')

        try:
            mail = utils.send_confirmation_email(request=request, user=user)
            if not mail:
                messages.error(request, "Не удалось отправить email")
                return redirect('users:settings')
            
            messages.success(
                request,
                'Регистрация успешна! Проверьте email для подтверждения. '
                'Вы сможете войти после подтверждения email.'
            )
            return redirect('users:settings')
            
        except Exception as e:
            messages.error(
                request,
                f'Ошибка при отправке письма: {str(e)}. Попробуйте позже.'
            )
            return redirect('users:register')
                

    def change_password(self, request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Обновление сессии, чтобы пользователь не разлогинился
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен')
            return redirect('users:settings')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            return render(request, self.template_name, {
                'password_form': form,
                'user': request.user
            })

