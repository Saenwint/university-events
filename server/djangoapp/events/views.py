import base64
from django.views import View
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect

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

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        if Ticket.objects.filter(user=request.user, event=event).exists():
            messages.error(request, 'Вы уже зарегистрированы на это мероприятие.')
            return redirect('events:event_detail', id=event.id)

        ticket = Ticket.objects.create(user=request.user, event=event)

        try:
            send_ticket_email(request, request.user, event, ticket)

            messages.success(
                request,
                f'Вы успешно зарегистрировались на мероприятие "{event.title}". '
                f'Билет выслан вам на почту.'
            )

            return redirect('events:event_detail', id=event.id)

        except Exception as e:
            ticket.delete()
            messages.error(
                request,
                'Ошибка при отправке билета. Попробуйте позже.'
            )

            return redirect('events:event_detail', id=event.id)