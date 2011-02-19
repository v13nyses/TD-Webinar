from django.conf import settings
from django import template
register = template.Library()

@register.inclusion_tag('events/recommend.html')
def recommend(request, recommend_form):
  return {'request': request, 'recommend_form': recommend_form, 'settings': settings}
