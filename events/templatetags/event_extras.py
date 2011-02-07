from django import template
from django.conf import settings
from django.template.loader import render_to_string

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

@register.simple_tag
def presentation(event):
  context = {
    'event': event,
    'settings': settings
  }

  return render_to_string(['events/presentation_%s.html' % event.state, 
                           'events/presentation.html'], context)
