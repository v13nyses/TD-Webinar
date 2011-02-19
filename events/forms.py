from django import forms
from models import Question

class QuestionForm(forms.ModelForm):
  class Meta:
    model = Question

class LoginForm(forms.Form):
  email = forms.EmailField(max_length=200)

class LogoutForm(forms.Form):
  logout = forms.CharField(widget=forms.HiddenInput, initial="false")

class RecommendForm(forms.Form):
  to_list = forms.EmailField(label="Friend's Email Address:")
