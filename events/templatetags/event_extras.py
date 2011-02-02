from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('events/presenter.html')
def presenter(presenter):
  return {
    'presenter': presenter,
    'settings': settings
  }

@register.inclusion_tag('events/presenter_list.html')
def presenter_list(presenters):
  return {
    'presenters': presenters,
    'settings': settings
  }

@register.inclusion_tag('events/presentation.html')
def presentation(event):
  return {
    'event': event,
    'settings': settings
  }
