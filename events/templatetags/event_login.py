from django.conf import settings
from django import template
register = template.Library()

@register.inclusion_tag('events/login.html')
def event_login(request, login_form, logout_form, event):
  return {'request': request, 'login_form': login_form, 'logout_form': logout_form, 'event': event, 'settings': settings}
