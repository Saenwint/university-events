from django.urls import path

from tickets.views import RegisterForEventView

urlpatterns = [
    path('register/<int:event_id>/', RegisterForEventView.as_view(), name='register_for_event'),
]