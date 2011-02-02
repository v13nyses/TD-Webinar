from form_utils.forms import BetterForm
from form_utils.widgets import AutoResizeTextarea
from events.models import Event, event_upload_to
from presentations.models import Video, Presentation, PresenterType, Presenter
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

class PresentationForm(BetterForm):
  presenter_type = forms.ChoiceField(choices = PresenterType.objects.all().values_list())
  full_name = forms.CharField()
  job_title = forms.CharField()
  photo = forms.FileField()
  bio = forms.CharField(widget = AutoResizeTextarea)
