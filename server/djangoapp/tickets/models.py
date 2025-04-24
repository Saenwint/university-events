import secrets
from io import BytesIO
from django.db import models
from django.utils import timezone
from datetime import timedelta

from events.models import Event
from users.models import User


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    unique_code = models.CharField(max_length=50, unique=True, blank=True)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата использования')
    qr_code_image = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.event.title}'

    def mark_as_used(self):
        """Отметка билета как использованного"""
        self.is_used = True
        self.used_at = timezone.now()
        self.save()
        
        if self.event.coins_reward > 0:
            self.user.add_coins(self.event.coins_reward)
        
        return True

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = f"EV-{self.event.id}-US-{self.user.id}-{secrets.token_urlsafe(8)}"

        if not self.qr_code_image:
            qr_data = self.generate_qr_data()
            qr_image = self.generate_qr_image(qr_data)
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            buffer.seek(0)
            self.qr_code_image = buffer.read()

        super().save(*args, **kwargs)

    def generate_qr_data(self):
        return f"EVENT:{self.event.id}:USER:{self.user.id}:CODE:{self.unique_code}"

    def is_pending(self):
        """
        Проверяет, находится ли билет в статусе "Ожидается".
        Билет ожидается, если текущее время меньше времени начала мероприятия.
        """
        event_time = self.event.date
        check_time = timezone.now()
        return check_time < event_time

    def is_expired(self):
        """
        Проверяет, просрочен ли билет.
        Билет считается просроченным, если текущее время больше времени окончания допустимого диапазона.
        """
        event_time = self.event.date
        check_time = timezone.now()
        return check_time > event_time + timedelta(hours=4)
    
    @staticmethod
    def generate_qr_image(data):
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")
    

class CoinTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coin_transactions')
    amount = models.IntegerField()
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created_at']
    