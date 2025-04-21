from django.views import View
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from tickets.models import Ticket
from events.utils import send_ticket_email
from events.models import Event
from events.forms import EventFilterForm


class EventListView(View):
    template_name = 'events/event_list.html'
    
    def get(self, request):
        events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
        
        form = EventFilterForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['significance_level']:
                events = events.filter(significance_level=form.cleaned_data['significance_level'])
            if form.cleaned_data['type']:
                events = events.filter(type=form.cleaned_data['type'])
            if form.cleaned_data['has_coins']:
                events = events.filter(coins_reward__gt=0)
        
        return render(request, self.template_name, {
            'events': events,
            'form': form
        })
    

class EventDetailView(View):
    template_name = 'events/event_detail.html'
    
    def get(self, request, id):
        event = get_object_or_404(Event, id=id)
        return render(request, self.template_name, {'event': event})
    

class RegisterForEventView(LoginRequiredMixin, View):
    login_url = '/users/login/'
    template_name = 'events/email_ticket.html'
    
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