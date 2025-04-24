from django.db.models.signals import post_save
from django.dispatch import receiver

from events.models import Event
from tickets.models import Ticket
from analytics.models import EventStats


@receiver(post_save, sender=Event)
def create_event_stats(sender, instance, created, **kwargs):
    if created:
        EventStats.objects.create(event=instance)

@receiver(post_save, sender=Ticket)
def update_event_stats(sender, instance, **kwargs):
    if hasattr(instance.event, 'stats'):
        instance.event.stats.update_stats()