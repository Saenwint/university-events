from django.urls import path

from tickets.views import ScanTicketView
from django.views.generic import RedirectView


app_name = 'tickets'

urlpatterns = [
    path('', RedirectView.as_view(url='/tickets/scan/', permanent=False)),
    path('scan/', ScanTicketView.as_view(), name='scan_ticket'),
]