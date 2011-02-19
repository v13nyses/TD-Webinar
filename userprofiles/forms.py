from django import forms
from userprofiles.models import UserProfile

class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    exclude = ('ip_address')
