from django.conf import settings
from django import template
register = template.Library()

@register.inclusion_tag('registration/register.html')
def event_register(request, register_event_form):
  return {'request': request, 'register_event_form': register_event_form, 'settings': settings}
