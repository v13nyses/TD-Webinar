from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('dashboard/presenter_pane.html')
def presenter_pane(event):
  return {
    'event': event,
    'settings': settings
  }

@register.inclusion_tag('dashboard/slide_pane.html')
def slide_pane(event):
  return {
    'event': event,
    'settings': settings,
    'slides': event.presentation.slide_set.slide_set.order_by('offset')
  }
