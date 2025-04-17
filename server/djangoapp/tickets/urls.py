from django.urls import path

from tickets.views import ScanTicketView

urlpatterns = [
    path('scan/', ScanTicketView.as_view(), name='scan_ticket'),
]