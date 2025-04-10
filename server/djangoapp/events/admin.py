from django.contrib import admin
from events.models import Event

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'significance_level')
    list_filter = ('significance_level', 'date')
    search_fields = ('title', 'short_description')