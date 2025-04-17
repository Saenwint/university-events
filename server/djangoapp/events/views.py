from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from django.utils import timezone
from django.urls import reverse_lazy

from events.models import Event
from events.forms import EventForm

# Create your views here.
class EventListView(View):
    template_name = 'main/home.html'
    
    def get(self, request):
        events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
        return render(request, self.template_name, {'events': events})

class EventDetailView(View):
    template_name = 'events/event.html'
    
    def get(self, request, id):
        event = get_object_or_404(Event, id=id)
        return render(request, self.template_name, {'event': event})