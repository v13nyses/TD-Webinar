from form_utils.forms import BetterForm, BetterModelForm
from form_utils.widgets import AutoResizeTextarea
from events.models import Event, event_upload_to
from presentations.models import Video, Presentation, PresenterType, Presenter, Slide
from django import forms
from django.template.loader import render_to_string
from django.forms.widgets import SplitDateTimeWidget, HiddenInput
from django.core.files.uploadedfile import InMemoryUploadedFile
import os, datetime
import ipdb
import form_fields

class EventForm(BetterModelForm):
  name = forms.CharField()
  short_description = forms.CharField(widget = AutoResizeTextarea())
  description = forms.CharField(widget = AutoResizeTextarea())

  lobby_start_date = forms.DateTimeField(widget = SplitDateTimeWidget())
  live_start_date = forms.DateTimeField(widget = SplitDateTimeWidget())
  live_stop_date = forms.DateTimeField(widget = SplitDateTimeWidget())
  archive_start_date = forms.DateTimeField(widget = SplitDateTimeWidget())

  lobby_video = form_fields.VideoField()
  image = forms.FileField(required = False)
  resource_guide = forms.FileField(required = False)

  class Meta:
    model = Event
    fieldsets = [('Event Details', {'fields': [
                    'name',
                    'lobby_start_date',
                    'live_start_date',
                    'live_stop_date',
                    'archive_start_date',
                    'short_description',
                    'description'
                  ]}),
                 ('Event Files', {'fields': [
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

class SlideForm(BetterModelForm):
  video = form_fields.VideoField(archive = True)
  image = forms.ImageField(required = False, widget = form_fields.ImageWidget)
  offset = form_fields.TimeOffsetField()

  class Meta:
    model = Slide

    fieldsets = [('Video', {'fields': ['video']}),
                 ('Add Slide', {'fields': [
                    'image',
                    'offset'
                ]})]
