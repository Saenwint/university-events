from django import forms

from events.models import Event


class EventFilterForm(forms.Form):
    significance_level = forms.ChoiceField(
        choices=[('', 'Все уровни')] + Event.SIGNIFICANCE_LEVELS,
        required=False,
        label='Уровень значимости'
    )
    type = forms.ChoiceField(
        choices=[('', 'Все типы')] + Event.EVENT_TYPES,
        required=False,
        label='Тип мероприятия'
    )
    has_coins = forms.BooleanField(
        required=False,
        label='Только с ЛЭТИ-коинами'
    )