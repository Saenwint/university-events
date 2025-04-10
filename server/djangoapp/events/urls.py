from django.urls import path
from events.views import EventListView, EventDetailView


urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('<int:id>/', EventDetailView.as_view(), name='event_detail'),
]