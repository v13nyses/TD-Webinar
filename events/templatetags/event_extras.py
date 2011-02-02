from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('events/presenter_list.html')
def presenters(presenters):
  return {
    'presenters': presenters,
    'settings': settings
  }
