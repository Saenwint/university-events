from django.db import models

from events.models import Event


class EventStats(models.Model):
    event = models.OneToOneField(
        Event, 
        on_delete=models.CASCADE,
        related_name='stats',
        primary_key=True
    )
    total_registered = models.PositiveIntegerField(default=0)
    total_attended = models.PositiveIntegerField(default=0)
    calculated_at = models.DateTimeField(auto_now=True)

    @property
    def attendance_percentage(self):
        if self.total_registered == 0:
            return 0
        return round((self.total_attended / self.total_registered) * 100, 2)

    @classmethod
    def generate_stats_report(cls, events):
        report_data = {
            'total_events': events.count(),
            'events': []
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
        
        return report_data