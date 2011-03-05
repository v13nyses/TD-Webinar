from django import template
from django.conf import settings
from presentations.models import Slide
import simplejson
from sorl.thumbnail import get_thumbnail

register = template.Library()

@register.inclusion_tag('presentations/video_player.html')
def video_player(video_id, player_id):
  url = settings.VIDEO_URL % (video_id, player_id)
  return {
    'url': url,
    'player_id': player_id,
    'video_id': video_id
  }

@register.inclusion_tag('presentations/slide.html')
def first_slide(event):
  slide = event.presentation.slide_set.slide_set.order_by('offset')[0]

  return {
    'slide': slide,
    'settings': settings
  }

@register.simple_tag
def slide_set_json(event):
  slides = event.presentation.slide_set.slide_set.order_by('offset')

  slides_data = []
  for slide in slides:
    # filter out slides if this is in the archive state
    if event.state == event.STATE_ARCHIVE:
      leaf = slide.as_leaf_class()
      if type(leaf) == Slide:
        slides_data.append({
          'slideId': slide.id,
          'timeOffset': slide.offset,
          'image': get_thumbnail(slide.image, '360x270').url
        })
    else:
      slides_data.append({
        'slideId': slide.id,
        'timeOffset': slide.offset,
        'image': get_thumbnail(slide.image, '360x270').url
      })

  return simplejson.dumps(slides_data)
