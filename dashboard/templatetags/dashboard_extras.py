from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('dashboard/presenter_pane.html')
def presenter_pane(event):
  return {
    'event': event,
    'settings': settings
  }

@register.simple_tag
def presenter_link(event, presenter, action = ''):
  if action == 'add':
    return '/dashboard/event/%d/presenters/add/' % event.id
  else:
    return '/dashboard/event/%d/presenter/%d/%s' % (event.id, presenter.id, action)
