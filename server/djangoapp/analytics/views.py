from django.utils import timezone
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from analytics.forms import EventFilterForm
from events.models import Event


class AnalyticsWelcomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/welcome.html'
    
    def test_func(self):
        return self.request.user.is_admin
    

class AnalyticsEventsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'analytics/analytics_events_list.html'
    context_object_name = 'events'

    def test_func(self):
        return self.request.user.is_admin

    def get_queryset(self):
        queryset = Event.objects.all()

        form = EventFilterForm(self.request.GET)
        if form.is_valid():
            event_type = form.cleaned_data.get('type')
            activity_type = form.cleaned_data.get('activity_type')
            status = form.cleaned_data.get('status')

            if event_type:
                queryset = queryset.filter(type=event_type)
            if activity_type:
                queryset = queryset.filter(activity_type=activity_type)
            if status == "Проведено":
                queryset = queryset.filter(date__lt=timezone.now())
            elif status == "Ожидается":
                queryset = queryset.filter(date__gte=timezone.now())

        sort_by = self.request.GET.get('sort_by', '-date')
        if sort_by in ['title', '-title', 'date', '-date']:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = EventFilterForm(self.request.GET or None)

        context['sort_by'] = self.request.GET.get('sort_by', '-date')

        return context
    

class AnalyticsEventView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'events/event_analytics.html'
    login_url = '/users/login/'

    def test_func(self):
        """Проверка, что пользователь администратор"""
        return self.request.user.is_admin

    def handle_no_permission(self):
        """Обработка отсутствия прав"""
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "Доступ к аналитике разрешен только администраторам")
        return redirect('events:event_list')

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        
        # Получаем статистику по мероприятию
        tickets = event.registrations.all()
        expired_tickets = [t for t in tickets if t.is_expired() and not t.is_used]
        
        context = {
            'event': event,
            'registered_tickets': tickets,
            'attended_tickets': tickets.filter(is_used=True),
            'missed_tickets': expired_tickets,
            'stats': event.stats,
        }
        return render(request, self.template_name, context)