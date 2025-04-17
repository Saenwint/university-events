from django import forms

from events.models import Event
from users.models import User

class RegistrationForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput())