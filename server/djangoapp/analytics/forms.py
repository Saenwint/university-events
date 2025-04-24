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
    
    PERIOD_CHOICES = [
        ('week', 'Неделя'),
        ('month', 'Месяц'),
        ('year', 'Год'),
        ('all', 'Весь период'),
    ]
    
    analysis_type = forms.ChoiceField(
        choices=ANALYSIS_TYPE_CHOICES,
        label='Тип анализа',
        widget=forms.Select(attrs={
            'onchange': "updateFormFields()",
            'class': 'form-control'
        })
    )
    
    activity_type = forms.ChoiceField(
        choices=[('', 'Все виды деятельности')] + Event.ACTIVITY_TYPES,
        required=False,
        label='Вид деятельности',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    event_type = forms.ChoiceField(
        choices=[('', 'Все типы мероприятий')] + Event.EVENT_TYPES,
        required=False,
        label='Тип мероприятия',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    period = forms.ChoiceField(
        choices=PERIOD_CHOICES,
        label='Период',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_range = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        required=False,
        label='Конкретная дата'
    )