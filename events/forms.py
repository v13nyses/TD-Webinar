from django import forms

class LoginForm(forms.Form):
  email = forms.EmailField(max_length=200)

class LogoutForm(forms.Form):
  logout = forms.CharField(widget=forms.HiddenInput, initial="false")

class RecommendForm(forms.Form):
  to_list = forms.EmailField(label="Friend's Email Address:")
