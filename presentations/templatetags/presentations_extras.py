from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('presentations/video_player.html')
def video_player(video_id, player_id):
  url = settings.VIDEO_URL % (video_id, player_id)
  return {
    'url': url
  }
