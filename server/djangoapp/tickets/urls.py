from django.urls import path

from tickets.views import RegisterForEventView, ScanTicketView

urlpatterns = [
    path('register/<int:event_id>/', RegisterForEventView.as_view(), name='register_for_event'),
    path('scan/', ScanTicketView.as_view(), name='scan_ticket'),
]