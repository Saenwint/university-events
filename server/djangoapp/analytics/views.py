from django.template.loader import render_to_string
from django.shortcuts import redirect
import os
from django.conf import settings
from django.utils import timezone
from django.views.generic import (
    TemplateView, 
    ListView, 
    FormView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import timedelta

from analytics.forms import EventFilterForm, AttendanceAnalysisForm
from events.models import Event


class AnalyticsWelcomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/welcome.html'
    
    def test_func(self):
        return self.request.user.is_admin
    

class AnalyticsEventsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'analytics/analytics_events/analytics_events_list.html'
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
                queryset = queryset.filter(date__lt=timezone.now() - timedelta(hours=4))
            elif status == "Ожидается":
                queryset = queryset.filter(date__gte=timezone.now() - timedelta(hours=4))
        
        sort_by = self.request.GET.get('sort_by', '-date')
        if sort_by in ['title', '-title', 'date', '-date']:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventFilterForm(self.request.GET or None)
        context['sort_by'] = self.request.GET.get('sort_by', '-date')
        context['current_time'] = timezone.now()
        return context
    

class AnalyticsEventView(LoginRequiredMixin, UserPassesTestMixin, View):
    ...
    

class AttendanceAnalysisView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'analytics/analytics_events/attendance_analysis.html'
    form_class = AttendanceAnalysisForm

    def test_func(self):
        return self.request.user.is_admin
    
    def form_valid(self, form):
        try:
            filters = {
                'activity_type': form.cleaned_data.get('activity_type'),
                'event_type': form.cleaned_data.get('event_type'),
                'period': form.cleaned_data.get('period'),
            }
            
            now = timezone.now()
            events = Event.objects.filter(date__lt=now - timedelta(hours=4))  # Только проведенные мероприятия
            
            # Применяем фильтры
            if filters['activity_type']:
                events = events.filter(activity_type=filters['activity_type'])
            
            if filters['event_type']:
                events = events.filter(type=filters['event_type'])
            
            if filters['period'] != 'all':
                if filters['period'] == 'week':
                    start_date = now - timedelta(days=7)
                elif filters['period'] == 'month':
                    start_date = now - timedelta(days=30)
                elif filters['period'] == 'year':
                    start_date = now - timedelta(days=365)
                else:
                    start_date = now - timedelta(days=365*10)  # На всякий случай
                
                events = events.filter(date__gte=start_date)
            
            # Если нет мероприятий
            if not events.exists():
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        no_events=True,
                        filters=filters
                    )
                )
            
            # Подготовка данных для отчета
            report_data = {
                'total_events': events.count(),
                'events': [],
                'filters': filters,
                'generated_at': now
            }
            
            for event in events:
                registered = event.registrations.count()
                attended = event.registrations.filter(is_used=True).count()
                percentage = round((attended / registered * 100), 2) if registered > 0 else 0
                
                report_data['events'].append({
                    'title': event.title,
                    'date': event.date,
                    'type': event.get_type_display(),
                    'activity_type': event.get_activity_type_display(),
                    'registered': registered,
                    'attended': attended,
                    'percentage': percentage
                })
            
            # Генерация HTML-отчета
            report_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
            os.makedirs(report_dir, exist_ok=True)
            report_filename = f"attendance_report_{now.strftime('%Y%m%d_%H%M%S')}.html"
            report_path = os.path.join(report_dir, report_filename)
            
            html_content = render_to_string(
                'analytics/analytics_events/attendance_report.html',
                {'report': report_data}
            )
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Проверяем, что файл создан
            if os.path.exists(report_path):
                return redirect(f"{settings.MEDIA_URL}reports/{report_filename}")
            else:
                raise Exception("Не удалось создать файл отчета")
                
        except Exception as e:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    error=str(e),
                    filters=filters
                )
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'no_events' in kwargs:
            context['no_events'] = kwargs['no_events']
        if 'error' in kwargs:
            context['error'] = kwargs['error']
        if 'filters' in kwargs:
            context['filters'] = kwargs['filters']
        return context