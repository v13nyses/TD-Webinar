from django.conf import settings
from django import template
register = template.Library()

@register.inclusion_tag('exitsurvey/thank_you.html')
def thank_you(request):
  return {'request': request, 'settings': settings}
