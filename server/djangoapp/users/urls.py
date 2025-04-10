from django.urls import path

from users.views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    ConfirmEmailView
)

urlpatterns = [
    path('confirm/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirm'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]