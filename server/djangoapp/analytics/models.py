from django.db import models

from events.models import Event


class EventStats(models.Model):
    PERIOD_CHOICES = [
        ('week', 'Неделя'),
        ('month', 'Месяц'),
        ('year', 'Год'),
        ('all', 'Весь период'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='stats')
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='all')
    total_registered = models.PositiveIntegerField(default=0)
    total_attended = models.PositiveIntegerField(default=0)
    calculation_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Статистика мероприятия'
        verbose_name_plural = 'Статистика мероприятий'
        ordering = ['-calculation_date']
    
    def __str__(self):
        return f"Статистика {self.event.title} за {self.get_period_display()}"

    def update_stats(self):
        """Обновляет статистику мероприятия"""
        self.total_registered = self.event.registrations.count()
        self.total_attended = self.event.registrations.filter(is_used=True).count()
        self.save()
        return self

    @property
    def attendance_rate(self):
        return round((self.total_attended / self.total_registered * 100), 2) if self.total_registered > 0 else 0
    
    @property
    def total_missed(self):
        """Количество не пришедших"""
        return self.total_registered - self.total_attended
