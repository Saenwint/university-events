import secrets
from django.db import models
from django.utils import timezone

from events.models import Event
from users.models import User

# Create your models here.
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    unique_code = models.CharField(max_length=50, unique=True, blank=True)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата использования')


    def __str__(self):
        return f'{self.user} - {self.event.title}'

    def mark_as_used(self):
        """Отметка билета как использованного"""
        self.is_used = True
        self.used_at = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = f"EV-{self.event.id}-US-{self.user.id}-{secrets.token_urlsafe(8)}"
        super().save(*args, **kwargs)

    def generate_qr_data(self):
        return f"EVENT:{self.event.id}:USER:{self.user.id}:CODE:{self.unique_code}"
    