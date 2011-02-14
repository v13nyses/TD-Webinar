from django.conf import settings
from django import template
register = template.Library()

@register.inclusion_tag('registration/register.html')
def event_register(request):
  return {'request': request}
