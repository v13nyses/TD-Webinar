from django.conf import settings
from django import template
register = template.Library()

print register
@register.inclusion_tag('userprofiles/user_profile.html')
def user_profile(request, user_profile_form):
  return {'request': request, 'user_profile_form': user_profile_form, 'settings': settings}
