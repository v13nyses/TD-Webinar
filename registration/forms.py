from django import forms

class RegisterForm(forms.Form):
  email = forms.CharField(max_length=200)
#  event = 

class LoginForm(forms.Form):
  pass
