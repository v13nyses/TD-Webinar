from django import forms
from events.models import Event

class RegisterEventForm(forms.Form):
  #email = forms.CharField(max_length=200, widget=forms.HiddenInput)
  #event = forms.ModelChoiceField(Event.objects.all(), widget=forms.HiddenInput)
  register = forms.CharField(widget=forms.HiddenInput, initial="false")

class LoginForm(forms.Form):
  pass
