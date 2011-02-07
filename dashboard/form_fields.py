import datetime
from django import forms
from django.template.loader import render_to_string
from presentations.models import Video

### http://djangosnippets.org/snippets/934/
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
import os
from sorl.thumbnail import get_thumbnail

def thumbnail(image_path):
    t = get_thumbnail(image_path, '112x100', crop='center')
    return u'<img src="%s" alt="%s" />' % (t.url, image_path)

class ImageWidget(forms.widgets.FileInput):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    def render(self, name, value, attrs=None):
        output = []
        if value and os.path.exists(str(value)):
           output.append(thumbnail(value)) 
        output.append(super(forms.widgets.FileInput, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

### /snippet-934

def parse_date_offset_string(offset_hms):
  offset_components = offset_hms.split(':')

  offset_seconds = 0
  for i in range(0, len(offset_components)):
    offset_seconds += int(offset_components[i]) * 60**(len(offset_components) - i - 1)

  return offset_seconds

def date_offset_string(offset_seconds):
  return str(datetime.timedelta(seconds = offset_seconds))

class VideoWidget(forms.MultiWidget):
  def __init__(self):
    self.widgets = (forms.TextInput(), forms.TextInput())
    forms.MultiWidget.__init__(self, self.widgets)

  def decompress(self, video_id):
    if type(video_id) == list:
      return video_id
    elif video_id:
      video = Video.objects.get(id = video_id)
      return [video.video_id, video.player_id]
    else:
      return [None, None]

  def render_widgets(self, name, value, attrs):
    rendered_widgets = []
    values = self.decompress(value)
    for i in range(0, len(self.widgets)):
      widget = self.widgets[i]
      widget_name = '%s_%d' % (name, i)
      widget_attrs = attrs
      widget_attrs['id'] = widget_name
      rendered_widgets.append(widget.render(widget_name, values[i], widget_attrs))

    return rendered_widgets

  def render(self, name, value, attrs = None):
    """ Add labels to the two video textinputs. """
    video_id, player_id = self.decompress(value)
    video_id_widget, player_id_widget = self.render_widgets(name, value, attrs)
    return render_to_string('dashboard/video_widget.html', {'video_id': video_id,
                                                        'player_id': player_id,
                                                        'video_id_widget': video_id_widget,
                                                        'player_id_widget': player_id_widget})

class TimeOffsetWidget(forms.widgets.TextInput):
  def render(self, name, value, attrs = None):
    if type(value) == unicode:
      offset_hms = value
    elif value:
      offset_hms = date_offset_string(value)
    else:
      offset_hms = value

    return forms.widgets.TextInput.render(self, name, offset_hms, attrs = attrs)

class TimeOffsetField(forms.CharField):
  def __init__(self):
    forms.CharField.__init__(self, widget = TimeOffsetWidget())

  def clean(self, value):
    offset_sec = parse_date_offset_string(value)
    return forms.CharField.clean(self, offset_sec)

class VideoField(forms.MultiValueField):
  def __init__(self):
    self.widget = VideoWidget()
    self.fields = (forms.CharField(), forms.CharField())
    forms.MultiValueField.__init__(self, self.fields)

  def clean(self, value, initial = None):
    value = super(VideoField, self).clean(value)
    return value
  
  def compress(self, value_list):
    if value_list:
      video_id, player_id = value_list
      try:
        video = Video.objects.get(video_id = video_id, player_id = player_id)
      except Video.DoesNotExist:
        video = Video()
        video.video_id = video_id
        video.player_id = player_id
        video.save()

      return video
    else:
      return None
