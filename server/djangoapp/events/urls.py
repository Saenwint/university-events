from django.urls import path
from events.views import EventListView, EventDetailView, RegisterForEventView

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('<int:id>/', EventDetailView.as_view(), name='event_detail'),
    path('<int:event_id>/register/', RegisterForEventView.as_view(), name='register'),
]