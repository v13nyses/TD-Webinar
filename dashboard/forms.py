from form_utils.forms import BetterForm, BetterModelForm
from form_utils.widgets import AutoResizeTextarea
from events.models import Event, event_upload_to
from presentations.models import Video, Presentation, PresenterType, Presenter, Slide
from eventmailer.models import mailchimp_template_choices
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
  image = forms.ImageField(required = False, widget = form_fields.ImageWidget)
  resource_guide = forms.FileField(required = False)
  slides = forms.FileField(required = False)
  timing = forms.FileField(required = False)
  outlook_file = forms.FileField(required = False)

  template_1_hour = forms.ChoiceField(choices = mailchimp_template_choices())
  template_24_hour = forms.ChoiceField(choices = mailchimp_template_choices())
  template_missed_you = forms.ChoiceField(choices = mailchimp_template_choices())
  template_thank_you = forms.ChoiceField(choices = mailchimp_template_choices())

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
                    'slides',
                    'timing',
                    'lobby_video'
                  ]}),
                 ('MailChimp Templates', {'fields': [
                    'template_1_hour',
                    'template_24_hour',
                    'template_missed_you',
                    'template_thank_you'
                 ]})]

class PresentationForm(BetterModelForm):
  presenter_type = forms.ChoiceField(choices = PresenterType.objects.all().values_list())
  name = forms.CharField()
  job_title = forms.CharField()
  photo = forms.ImageField(required = False, widget = form_fields.ImageWidget)
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

  slide_type = forms.ChoiceField(choices = [('slide', 'Slide'), ('poll', 'Poll')])
  poll_question = forms.CharField(required = False)
  poll_choices = forms.CharField(widget = AutoResizeTextarea, required = False)

  class Meta:
    model = Slide

    fieldsets = [('Video', {'fields': ['video']}),
                 ('Add Slide', {'fields': [
                    'slide_type',
                    'image',
                    'offset',
                    'poll_question',
                    'poll_choices'
                ]})]
