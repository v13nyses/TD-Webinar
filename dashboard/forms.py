from form_utils.forms import BetterForm
from form_utils.widgets import AutoResizeTextarea
from events.models import Event, event_upload_to
from presentations.models import Video, Presentation
from django import forms
from django.forms.widgets import SplitDateTimeWidget
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

class EventForm(BetterForm):
  name = forms.CharField()
  short_description = forms.CharField(widget = AutoResizeTextarea())
  description = forms.CharField(widget = AutoResizeTextarea())

  lobby_start_date = forms.DateTimeField(widget = SplitDateTimeWidget(),
                                input_formats = ['%m/%d/%Y %I:%M %p', '%m/%d/%Y %I:%M%p'])
  live_start_date = forms.DateTimeField(widget = SplitDateTimeWidget(),
                                input_formats = ['%m/%d/%Y %I:%M %p', '%m/%d/%Y %I:%M%p'])
  live_stop_date = forms.DateTimeField(widget = SplitDateTimeWidget(),
                                input_formats = ['%m/%d/%Y %I:%M %p', '%m/%d/%Y %I:%M%p'])
  archive_start_date = forms.DateTimeField(widget = SplitDateTimeWidget(),
                                input_formats = ['%m/%d/%Y %I:%M %p', '%m/%d/%Y %I:%M%p'])

  lobby_video = forms.CharField()
  image = forms.FileField()
  resource_guide = forms.FileField()

  def save(self):
    event = Event()

    for field_name in self.cleaned_data:
      field_value = self.cleaned_data[field_name]
      if field_name == 'lobby_video':
        video_id, player_id = field_value.split('-')
        video = Video()
        video.video_id = video_id
        video.player_id = player_id
        video.save()
        event.lobby_video = video
      elif type(field_value) == InMemoryUploadedFile:
        filepath = self.upload_file(event, field_value)
        event.__dict__[field_name] = filepath
      else:
        event.__dict__[field_name] = field_value
    
    presentation = Presentation()
    presentation.save()
    event.presentation = presentation

    event.save()
  
  def upload_file(self, event, uploaded_file):
    filepath = event_upload_to(event, uploaded_file.name)

    try:
      destination = open(filepath, 'wb+')
    except IOError:
      os.mkdir(os.path.dirname(filepath))
      destination = open(filepath, 'wb+')

    for chunk in uploaded_file.chunks():
      destination.write(chunk)
    destination.close()

    return filepath
    

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
