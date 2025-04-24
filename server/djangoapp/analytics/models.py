from django.db import models

from events.models import Event


class EventStats(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='stats')
    total_registered = models.PositiveIntegerField(default=0)
    total_attended = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Статистика мероприятия'
        verbose_name_plural = 'Статистика мероприятий'

    def update_stats(self):
        """Обновляет статистику мероприятия"""
        self.total_registered = self.event.registrations.count()
        self.total_attended = self.event.registrations.filter(is_used=True).count()
        self.save()
        return self

    @property
    def total_missed(self):
        """Количество не пришедших"""
        return self.total_registered - self.total_attended

    def __str__(self):
        return f"Статистика для {self.event.title}"