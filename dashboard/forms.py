from form_utils.forms import BetterForm, BetterModelForm
from form_utils.widgets import AutoResizeTextarea
from events.models import Event, event_upload_to
from presentations.models import Video, Presentation, PresenterType, Presenter
from django import forms
from django.forms.widgets import SplitDateTimeWidget, HiddenInput
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

class EventForm(BetterModelForm):
  name = forms.CharField()
  short_description = forms.CharField(widget = AutoResizeTextarea())
  description = forms.CharField(widget = AutoResizeTextarea())

  lobby_start_date = forms.DateTimeField(widget = SplitDateTimeWidget())
  live_start_date = forms.DateTimeField(widget = SplitDateTimeWidget())
  live_stop_date = forms.DateTimeField(widget = SplitDateTimeWidget())
  archive_start_date = forms.DateTimeField(widget = SplitDateTimeWidget())

  lobby_video_string = forms.CharField(required = False)
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
                    'lobby_video_string'
                  ]})]

class PresentationForm(BetterModelForm):
  presenter_type = forms.ChoiceField(choices = PresenterType.objects.all().values_list())
  name = forms.CharField()
  job_title = forms.CharField()
  photo = forms.FileField(required = False)
  description = forms.CharField(widget = AutoResizeTextarea)
  
  class Meta:
    model = Presenter
