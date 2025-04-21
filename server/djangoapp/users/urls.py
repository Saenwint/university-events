from django.urls import path
from django.views.generic import RedirectView

from users.views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    ConfirmEmailView,
    UserEventsView
)

app_name = 'users'

urlpatterns = [
    path('', RedirectView.as_view(url='/users/login', permanent=False)),
    path('confirm/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirm'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my_events/', UserEventsView.as_view(), name='my_events')
]