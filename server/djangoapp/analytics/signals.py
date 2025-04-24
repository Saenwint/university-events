from django.db.models.signals import post_save
from django.dispatch import receiver

from events.models import Event
from analytics.models import EventStats


@receiver(post_save, sender=Event)
def update_event_stats(sender, instance, **kwargs):
    EventStats.update_or_create_stats(instance)