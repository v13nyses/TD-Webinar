import datetime
from django import forms
from django.template.loader import render_to_string
from presentations.models import Video

### http://djangosnippets.org/snippets/934/
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
import os, ipdb
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
  if offset_hms != '':
    offset_components = offset_hms.split(':')
    offset_seconds = 0
    for i in range(0, len(offset_components)):
      offset_seconds += int(offset_components[i]) * 60**(len(offset_components) - i - 1)

    return offset_seconds

  else:
    return 0

def date_offset_string(offset_seconds):
  return str(datetime.timedelta(seconds = offset_seconds))

class VideoWidget(forms.MultiWidget):
  def __init__(self, archive = False):
    self.archive = archive
    if archive:
      self.widgets = (forms.TextInput(), forms.TextInput(), forms.TextInput())
    else:
      self.widgets = (forms.TextInput(), forms.TextInput())

    forms.MultiWidget.__init__(self, self.widgets)

  def decompress(self, video_id):
    if type(video_id) == list:
      return video_id
    elif video_id:
      video = Video.objects.get(id = video_id)
      if self.archive:
        return [video.video_id, video.player_id, video.archive_player_id]
      else:
        return [video.video_id, video.player_id]
    else:
      if self.archive:
        return [None] * 3
      return [None] * 2

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
    values = self.decompress(value)
    widgets = self.render_widgets(name, value, attrs)

    context = {
        'video_widget': widgets[0],
        'player_widget': widgets[1],
        'video_id': values[0],
        'player_id': values[1],
        'archive': self.archive
    }
    if len(widgets) == 3:
      context['archive_player_widget'] = widgets[2]
      context['archive_player_id'] = values[2]

    return render_to_string('dashboard/video_widget.html', context)

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
  def __init__(self, archive = False):
    self.widget = VideoWidget(archive = archive)
    self.archive = archive
    if archive:
      self.fields = (forms.CharField(), forms.CharField(), forms.CharField())
    else:
      self.fields = (forms.CharField(), forms.CharField())
    forms.MultiValueField.__init__(self, self.fields)

  def clean(self, value, initial = None):
    value = super(VideoField, self).clean(value)
    return value
  
  def compress(self, value_list):
    if value_list:
      if self.archive:
        video_id, player_id, archive_player_id = value_list
      else:
        video_id, player_id = value_list

      try:
        if self.archive:
          video = Video.objects.get(video_id = video_id, player_id = player_id, archive_player_id = archive_player_id)
        else:
          video = Video.objects.get(video_id = video_id, player_id = player_id)
      except Video.DoesNotExist:
        video = Video()
        video.video_id = video_id
        video.player_id = player_id
        if self.archive:
          video.archive_player_id = archive_player_id
        video.save()

      return video
    else:
      return None
