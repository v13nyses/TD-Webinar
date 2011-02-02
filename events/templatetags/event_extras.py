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
def presenter_list(presenter_list):
  return {
    'presenters': presenters,
    'settings': settings
  }

