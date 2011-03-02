from django import forms
from userprofiles.models import UserProfile

class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    exclude = ('ip_address', 'first_name', 'last_name', 'city', 'province', 'postal_code')
