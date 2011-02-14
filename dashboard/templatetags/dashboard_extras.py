from django import template
from django.conf import settings
from dashboard.form_fields import date_offset_string

register = template.Library()

@register.inclusion_tag('dashboard/presenter_pane.html')
def presenter_pane(event):
  return {
    'event': event,
    'settings': settings
  }

@register.inclusion_tag('dashboard/slide_pane.html')
def slide_pane(event):
  slide_set = event.presentation.slide_set
  slides = []
  if slide_set:
    slides = slide_set.slide_set.order_by('offset')

  return {
    'event': event,
    'settings': settings,
    'slides': slides
  }

@register.simple_tag
def time_offset(offset_seconds):
  return date_offset_string(offset_seconds)

@register.inclusion_tag('dashboard/form_buttons.html')
def form_buttons(name, back_button = True, save_buttons = True, continue_button = True):
  return {
    'name': name,
    'back_button': back_button,
    'continue_button': continue_button,
    'save_buttons': save_buttons
  }
