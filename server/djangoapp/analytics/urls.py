from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from analytics.views import (
    AnalyticsWelcomeView, 
    AnalyticsEventsListView,
    AnalyticsEventView,
    AttendanceAnalysisView
)

app_name = 'analytics'

urlpatterns = [
    path('', AnalyticsWelcomeView.as_view(), name='welcome'),
    path('events/', AnalyticsEventsListView.as_view(), name='analytics_events_list'),
    path('events/<int:event_id>/', AnalyticsEventView.as_view(), name='analytics_event_detail'),
    path('attendance/', AttendanceAnalysisView.as_view(), name='attendance_analysis'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)