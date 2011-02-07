from django import template
from django.conf import settings
from presentations.models import Slide

register = template.Library()

@register.inclusion_tag('presentations/video_player.html')
def video_player(video_id, player_id):
  url = settings.VIDEO_URL % (video_id, player_id)
  return {
    'url': url
  }

@register.inclusion_tag('presentations/slide.html')
def first_slide(event):
  slide = Slide.objects.order_by('offset')[0]

  return {
    'slide': slide,
    'settings': settings
  }
