from form_utils.forms import BetterForm, BetterModelForm
from form_utils.widgets import AutoResizeTextarea
from events.models import Event, event_upload_to
from presentations.models import Video, Presentation, PresenterType, Presenter
from django import forms
from django.template.loader import render_to_string
from django.forms.widgets import SplitDateTimeWidget, HiddenInput
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

class VideoWidget(forms.MultiWidget):
  def __init__(self):
    self.widgets = (forms.TextInput(), forms.TextInput())
    forms.MultiWidget.__init__(self, self.widgets)

  def decompress(self, video_id):
    if video_id:
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
    video_id, player_id = self.render_widgets(name, value, attrs)
    return render_to_string('dashboard/video_widget.html', {'video_id': video_id,
                                                            'player_id': player_id})

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

class EventForm(BetterModelForm):
  name = forms.CharField()
  short_description = forms.CharField(widget = AutoResizeTextarea())
  description = forms.CharField(widget = AutoResizeTextarea())

  lobby_start_date = forms.DateTimeField(widget = SplitDateTimeWidget())
  live_start_date = forms.DateTimeField(widget = SplitDateTimeWidget())
  live_stop_date = forms.DateTimeField(widget = SplitDateTimeWidget())
  archive_start_date = forms.DateTimeField(widget = SplitDateTimeWidget())

  lobby_video = VideoField()
  image = forms.FileField(required = False)
  resource_guide = forms.FileField(required = False)

  class Meta:
    model = Event
    fieldsets = [('details', {'fields': [
                    'name',
                    'lobby_start_date',
                    'live_start_date',
                    'live_stop_date',
                    'archive_start_date',
                    'short_description',
                    'description'
                  ]}),
                 ('files', {'fields': [
                    'image',
                    'resource_guide',
                    'lobby_video'
                  ]})]

class PresentationForm(BetterModelForm):
  presenter_type = forms.ChoiceField(choices = PresenterType.objects.all().values_list())
  name = forms.CharField()
  job_title = forms.CharField()
  photo = forms.FileField(required = False)
  description = forms.CharField(widget = AutoResizeTextarea)
  
  class Meta:
    model = Presenter

    fieldsets = [('Presenter', {'fields': [
                    'name',
                    'presenter_type',
                    'job_title',
                    'photo',
                    'description'
                ]})]
