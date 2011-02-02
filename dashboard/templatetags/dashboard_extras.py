from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('dashboard/presenter_pane.html')
def presenter_pane(event):
  return {
    'event': event,
    'settings': settings
  }
