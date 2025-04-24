from django import forms

from analytics.models import EventStats
from events.models import Event


class EventFilterForm(forms.Form):
    type = forms.ChoiceField(
        choices=[('', 'Все типы')] + Event.EVENT_TYPES,
        required=False,
        label='Тип мероприятия'
    )
    activity_type = forms.ChoiceField(
        choices=[('', 'Все виды')] + Event.ACTIVITY_TYPES,
        required=False,
        label='Тип деятельности'
    )
    status = forms.ChoiceField(
        choices=[
            ('', 'Все статусы'),
            ('Проведено', 'Проведено'),
            ('Ожидается', 'Ожидается'),
        ],
        required=False,
        label='Статус'
    )


class AttendanceAnalysisForm(forms.Form):
    ANALYSIS_TYPE_CHOICES = [
        ('activity', 'По виду деятельности'),
        ('type', 'По типу мероприятия'),
    ]
    
    analysis_type = forms.ChoiceField(
        choices=ANALYSIS_TYPE_CHOICES,
        label='Тип анализа'
    )
    
    period = forms.ChoiceField(
        choices=EventStats.PERIOD_CHOICES,
        label='Период'
    )
    
    date_range = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label='Конкретная дата (для недели/месяца)'
    )