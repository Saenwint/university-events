from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.utils import timezone

from events.models import Event

# Create your views here.
class HomeView(View):
    template_name = 'main/home.html'

    def get(self, request):
        upcoming_events = Event.objects.filter(
            date__gte=timezone.now()
        ).order_by('date')[:6]
        
        return render(request, self.template_name, {
            'events': upcoming_events
        })