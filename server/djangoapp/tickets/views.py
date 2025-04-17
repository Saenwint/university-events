from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render

from events.models import Event
from tickets.models import Ticket
from tickets.utils import send_ticket_email

class RegisterForEventView(LoginRequiredMixin, View):
    template_name = 'tickets/ticket_email.html'
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        
        if Ticket.objects.filter(user=request.user, event=event).exists():
            return JsonResponse(
                {'status': 'error', 'message': 'Вы уже зарегистрированы на это мероприятие'},
                status=400
            )
        
        ticket = Ticket.objects.create(user=request.user, event=event)
        
        try:
            send_ticket_email(request, request.user, event, ticket)
            return render(self.request, self.template_name)
        except Exception as e:
            ticket.delete()
            return JsonResponse(
                {'status': 'error', 'message': 'Ошибка при отправке билета. Попробуйте позже.'},
                status=500
            )