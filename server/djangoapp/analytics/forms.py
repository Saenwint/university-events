from django import forms

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